"""Pagination configuration — centralized config, no direct env reads.

Pagination settings are resolved through the centralized ``ConfigurationProviderPort``
(EN-0202 / ADR-0013) and validated at startup so that invalid values fail loudly
before the first list request reaches a router.

The preferred initialisation path is for the composition root (``lifespan.py``) to
call ``init_pagination_settings(provider)`` at startup, passing the already-validated
concrete provider.  ``get_pagination_settings()`` falls back to constructing
``RuntimeConfigurationProvider()`` lazily when the singleton has not been seeded yet
(useful in tests that reset + monkeypatch before the first call).

For tests, call ``reset_pagination_settings()`` (which also calls
``reset_runtime_settings()`` internally) to ensure a clean state.
"""

from __future__ import annotations

from baku.backend.application.configuration.errors import AggregatedConfigurationError
from baku.backend.application.configuration.provider_port import ConfigurationProviderPort


class PaginationSettings:
    """Projection of pagination-related keys from the centralized configuration profile.

    All access to configuration values is delegated to the centralized provider;
    no direct ``os.getenv`` calls are made here (ADR-0013).

    Invariants enforced at construction time (startup-fail semantics):
      - ``default_page_size >= 1``
      - ``max_page_size >= 1``

    When ``max_page_size < default_page_size``, the router capping logic will
    effectively use ``max_page_size`` as the operative default for uncapped
    requests. This is an intentional operator configuration choice.

    Raises:
        AggregatedConfigurationError: if any pagination config value is invalid.
    """

    def __init__(self, provider: ConfigurationProviderPort) -> None:
        profile = provider.get_profile()
        errors: list[str] = []

        raw_default = profile.require("pagination.default_page_size")
        raw_max = profile.require("pagination.max_page_size")

        try:
            self.default_page_size: int = int(raw_default)
        except (TypeError, ValueError):
            errors.append(
                f"'pagination.default_page_size' must be an integer; got '{raw_default}'."
            )
            self.default_page_size = 0  # placeholder so subsequent checks can run

        try:
            self.max_page_size: int = int(raw_max)
        except (TypeError, ValueError):
            errors.append(
                f"'pagination.max_page_size' must be an integer; got '{raw_max}'."
            )
            self.max_page_size = 0  # placeholder so subsequent checks can run

        if not errors:
            if self.default_page_size < 1:
                errors.append(
                    f"'pagination.default_page_size' must be >= 1; got {self.default_page_size}."
                )
            if self.max_page_size < 1:
                errors.append(
                    f"'pagination.max_page_size' must be >= 1; got {self.max_page_size}."
                )

        if errors:
            raise AggregatedConfigurationError(errors=errors)


_settings: PaginationSettings | None = None


def init_pagination_settings(provider: ConfigurationProviderPort) -> None:
    """Seed the singleton with an explicitly injected provider.

    Called by the composition root (``lifespan.py``) at startup so that the
    concrete ``RuntimeConfigurationProvider`` is never imported at the module
    level of this file.
    """
    global _settings
    _settings = PaginationSettings(provider)


def get_pagination_settings() -> PaginationSettings:
    """Return the process-level pagination settings singleton.

    Falls back to constructing ``RuntimeConfigurationProvider()`` lazily when
    the singleton has not been seeded yet (useful in tests that reset +
    monkeypatch before the first call).
    """
    global _settings
    if _settings is None:
        # Late import keeps this module's top-level dependencies confined to the
        # Application layer.  The composition root should call
        # init_pagination_settings() explicitly; this path exists so that tests
        # that reset + monkeypatch can call get_pagination_settings() without a
        # prior init_pagination_settings() call.
        from baku.backend.infrastructure.config.runtime_settings import (  # noqa: PLC0415
            RuntimeConfigurationProvider,
        )

        _settings = PaginationSettings(RuntimeConfigurationProvider())
    return _settings


def reset_pagination_settings() -> None:
    """Reset singleton — for use in tests only.

    Also resets the underlying centralized provider cache so that
    ``monkeypatch.setenv`` / ``monkeypatch.delenv`` take effect on the next
    ``get_pagination_settings()`` call.
    """
    global _settings
    _settings = None
    from baku.backend.infrastructure.config.runtime_settings import (  # noqa: PLC0415
        reset_runtime_settings,
    )

    reset_runtime_settings()
