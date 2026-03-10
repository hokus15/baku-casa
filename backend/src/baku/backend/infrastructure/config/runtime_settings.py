"""Concrete configuration provider implementation (EN-0202 / ADR-0013).

This module is the single Infrastructure class that implements
``ConfigurationProviderPort``.  It orchestrates the source loaders,
resolver and validator into one startup-time operation.

The resolved and validated ``ResolvedConfigurationProfile`` is cached as a
module-level singleton for the lifetime of the process.

Test helpers:
    ``reset_runtime_settings()`` clears the singleton, allowing tests to
    inject arbitrary environments via ``monkeypatch.setenv``.
"""

from __future__ import annotations

from pathlib import Path

from baku.backend.application.configuration.errors import (
    AggregatedConfigurationError,
)
from baku.backend.application.configuration.models import (
    ConfigurationIssueSeverity,
    ConfigurationParameterDefinition,
    ResolvedConfigurationProfile,
)
from baku.backend.application.configuration.provider_port import (
    ConfigurationProviderPort,
)
from baku.backend.infrastructure.config.resolver import resolve
from baku.backend.infrastructure.config.sources import (
    load_default_source,
    load_env_source,
    load_file_source,
)
from baku.backend.infrastructure.config.validator import validate

# ---------------------------------------------------------------------------
# Parameter registry — declare all known configuration keys here.
# ---------------------------------------------------------------------------

_PARAMETER_DEFINITIONS: list[ConfigurationParameterDefinition] = [
    ConfigurationParameterDefinition(
        key="persistence.database_url",
        required=False,
        default="sqlite:///./baku.db",
        description="SQLAlchemy database URL.  Defaults to a file-based SQLite DB.",
    ),
    ConfigurationParameterDefinition(
        key="auth.jwt_secret",
        required=True,
        description=(
            "JWT signing secret.  Must be a strong random value in production. "
            "Never hard-code.  See ADR-0005."
        ),
    ),
    ConfigurationParameterDefinition(
        key="auth.jwt_algorithm",
        required=False,
        description="JWT signing algorithm (e.g. HS256, RS256).",
    ),
    ConfigurationParameterDefinition(
        key="auth.token_ttl_seconds",
        required=False,
        description="Access token time-to-live in seconds.",
    ),
    ConfigurationParameterDefinition(
        key="auth.max_failed_attempts",
        required=False,
        description="Maximum consecutive failed login attempts before lockout.",
    ),
    ConfigurationParameterDefinition(
        key="auth.lockout_minutes",
        required=False,
        description="Operator account lockout duration in minutes.",
    ),
    ConfigurationParameterDefinition(
        key="pagination.default_page_size",
        required=False,
        default="20",
        description="Default page size for paginated list endpoints (ADR-0013).",
    ),
    ConfigurationParameterDefinition(
        key="pagination.max_page_size",
        required=False,
        default="100",
        description="Maximum allowed page size for paginated list endpoints (ADR-0013).",
    ),
]

# ---------------------------------------------------------------------------
# Singleton implementation
# ---------------------------------------------------------------------------

_profile: ResolvedConfigurationProfile | None = None


class RuntimeConfigurationProvider(ConfigurationProviderPort):
    """Infrastructure implementation of ``ConfigurationProviderPort``.

    Resolves and validates configuration exactly once at startup.  The result
    is cached in a module-level singleton.

    Args:
        env_file: Optional path to a .env file.  Defaults to the standard
            backend-root ``.env`` location.  Pass ``Path("")`` to disable
            file loading (useful in tests that inject everything via env vars).
    """

    def __init__(self, env_file: Path | None = None) -> None:
        self._env_file = env_file

    def get_profile(self) -> ResolvedConfigurationProfile:
        global _profile
        if _profile is None:
            _profile = self._build_profile()
        return _profile

    def _build_profile(self) -> ResolvedConfigurationProfile:
        env_source = load_env_source()
        file_source = load_file_source(self._env_file)
        default_source = load_default_source()

        profile = resolve(env_source, file_source, default_source)
        issues = validate(profile, _PARAMETER_DEFINITIONS)
        error_messages = [
            i.message
            for i in issues
            if i.severity == ConfigurationIssueSeverity.ERROR
        ]
        if error_messages:
            raise AggregatedConfigurationError(errors=error_messages)
        return profile


def get_runtime_provider(
    env_file: Path | None = None,
) -> RuntimeConfigurationProvider:
    """Return the process-level ``RuntimeConfigurationProvider`` singleton."""
    return RuntimeConfigurationProvider(env_file=env_file)


def reset_runtime_settings() -> None:
    """Clear the cached profile — for use in tests only."""
    global _profile
    _profile = None
