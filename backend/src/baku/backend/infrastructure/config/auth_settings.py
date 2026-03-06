"""Authentication policy configuration — centralized config, no direct env reads.

Auth settings are now resolved through the centralized ``ConfigurationProviderPort``
(EN-0202 / ADR-0013).  This module retains the same public API (``get_auth_settings`` /
``reset_auth_settings``) so that all callers in the Infrastructure and Interfaces
layers continue to work without change.

The singleton lock has been removed.  The ``RuntimeConfigurationProvider`` carries
its own module-level cache; ``AuthSettings`` is now a thin projection on top of it.

For tests, call both ``reset_auth_settings()`` and ``reset_runtime_settings()`` to
ensure a clean state.
"""

from __future__ import annotations

from baku.backend.infrastructure.config.runtime_settings import (
    RuntimeConfigurationProvider,
    reset_runtime_settings,
)


class AuthSettings:
    """Projection of auth-related keys from the centralized configuration profile.

    All access to env vars is delegated to the centralized provider; no direct
    ``os.getenv`` calls are made here (ADR-0013).

    Raises:
        AggregatedConfigurationError: propagated from the centralized provider
            when required keys (e.g. ``auth.jwt_secret``) are absent.
    """

    def __init__(self, provider: RuntimeConfigurationProvider | None = None) -> None:
        if provider is None:
            provider = RuntimeConfigurationProvider()
        profile = provider.get_profile()

        self.jwt_secret: str = profile.require("auth.jwt_secret")
        self.jwt_algorithm: str = profile.require("auth.jwt_algorithm")
        self.token_ttl_seconds: int = int(profile.require("auth.token_ttl_seconds"))
        self.max_failed_attempts: int = int(profile.require("auth.max_failed_attempts"))
        self.lockout_minutes: int = int(profile.require("auth.lockout_minutes"))


_settings: AuthSettings | None = None


def get_auth_settings() -> AuthSettings:
    global _settings
    if _settings is None:
        _settings = AuthSettings()
    return _settings


def reset_auth_settings() -> None:
    """Reset singleton — for use in tests only.

    Also resets the underlying centralized provider cache so that
    ``monkeypatch.setenv`` / ``monkeypatch.delenv`` take effect.
    """
    global _settings
    _settings = None
    reset_runtime_settings()
