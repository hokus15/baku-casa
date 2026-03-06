"""Authentication policy configuration — centralized config, no direct env reads.

Auth settings are now resolved through the centralized ``ConfigurationProviderPort``
(EN-0202 / ADR-0013).  This module retains the same public API (``get_auth_settings`` /
``reset_auth_settings``) so that all callers in the Infrastructure and Interfaces
layers continue to work without change.

The preferred initialisation path is for the composition root (``main.py``) to call
``init_auth_settings(provider)`` at startup, passing the already-validated concrete
provider.  ``get_auth_settings()`` falls back to constructing
``RuntimeConfigurationProvider()`` lazily when the singleton has not been seeded yet
(useful in tests that reset + monkeypatch before the first call).

This module's top-level imports depend only on the Application layer port; the
concrete Infrastructure class is loaded late, inside the fallback path only.

For tests, call both ``reset_auth_settings()`` and ``reset_runtime_settings()`` to
ensure a clean state.
"""

from __future__ import annotations

from baku.backend.application.configuration.provider_port import ConfigurationProviderPort


class AuthSettings:
    """Projection of auth-related keys from the centralized configuration profile.

    All access to env vars is delegated to the centralized provider; no direct
    ``os.getenv`` calls are made here (ADR-0013).

    Raises:
        AggregatedConfigurationError: propagated from the centralized provider
            when required keys (e.g. ``auth.jwt_secret``) are absent.
    """

    def __init__(self, provider: ConfigurationProviderPort) -> None:
        profile = provider.get_profile()

        self.jwt_secret: str = profile.require("auth.jwt_secret")
        self.jwt_algorithm: str = profile.require("auth.jwt_algorithm")
        self.token_ttl_seconds: int = int(profile.require("auth.token_ttl_seconds"))
        self.max_failed_attempts: int = int(profile.require("auth.max_failed_attempts"))
        self.lockout_minutes: int = int(profile.require("auth.lockout_minutes"))


_settings: AuthSettings | None = None


def init_auth_settings(provider: ConfigurationProviderPort) -> None:
    """Seed the singleton with an explicitly injected provider.

    Called by the composition root (``main.py``) at startup so that the
    concrete ``RuntimeConfigurationProvider`` is never imported at the module
    level of this file.
    """
    global _settings
    _settings = AuthSettings(provider)


def get_auth_settings() -> AuthSettings:
    global _settings
    if _settings is None:
        # Fallback: late import keeps this module's top-level dependencies
        # confined to the Application layer.  The composition root should
        # call init_auth_settings() explicitly; this path exists so that
        # tests that reset + monkeypatch can call get_auth_settings() without
        # a prior init_auth_settings() call.
        from baku.backend.infrastructure.config.runtime_settings import (  # noqa: PLC0415
            RuntimeConfigurationProvider,
        )

        _settings = AuthSettings(RuntimeConfigurationProvider())
    return _settings


def reset_auth_settings() -> None:
    """Reset singleton — for use in tests only.

    Also resets the underlying centralized provider cache so that
    ``monkeypatch.setenv`` / ``monkeypatch.delenv`` take effect on the next
    ``get_auth_settings()`` call.
    """
    global _settings
    _settings = None
    from baku.backend.infrastructure.config.runtime_settings import (  # noqa: PLC0415
        reset_runtime_settings,
    )

    reset_runtime_settings()
