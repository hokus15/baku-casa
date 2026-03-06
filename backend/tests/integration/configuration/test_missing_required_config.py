"""Integration test: fail-fast on missing required keys (EN-0202 US2).

Tests that the startup validator raises ``AggregatedConfigurationError``
when one or more required configuration keys are absent.
"""

from __future__ import annotations

import pytest

from baku.backend.application.configuration.errors import AggregatedConfigurationError
from baku.backend.infrastructure.config.runtime_settings import (
    RuntimeConfigurationProvider,
    reset_runtime_settings,
)


@pytest.fixture(autouse=True)
def _reset_provider():
    reset_runtime_settings()
    yield
    reset_runtime_settings()


def test_raises_when_required_key_missing(monkeypatch, tmp_path):
    """Startup fails when AUTH_JWT_SECRET is absent from all sources."""
    monkeypatch.delenv("AUTH_JWT_SECRET", raising=False)
    # Use a tmp_path env_file that does not exist -> file source is empty
    provider = RuntimeConfigurationProvider(env_file=tmp_path / ".env")

    with pytest.raises(AggregatedConfigurationError) as exc_info:
        provider.get_profile()

    error = exc_info.value
    assert "auth.jwt_secret" in str(error)


def test_error_mentions_missing_key_name(monkeypatch, tmp_path):
    """The aggregated error message names the missing key explicitly."""
    monkeypatch.delenv("AUTH_JWT_SECRET", raising=False)

    provider = RuntimeConfigurationProvider(env_file=tmp_path / ".env")

    with pytest.raises(AggregatedConfigurationError) as exc_info:
        provider.get_profile()

    assert "auth.jwt_secret" in str(exc_info.value)
    assert "missing" in str(exc_info.value).lower()


def test_does_not_cache_failed_profile(monkeypatch, tmp_path):
    """A failed validation does not cache a partial profile."""
    monkeypatch.delenv("AUTH_JWT_SECRET", raising=False)

    provider = RuntimeConfigurationProvider(env_file=tmp_path / ".env")

    with pytest.raises(AggregatedConfigurationError):
        provider.get_profile()

    # Reset and provide the key — provider must recover.
    reset_runtime_settings()
    monkeypatch.setenv("AUTH_JWT_SECRET", "recovered-secret")

    provider2 = RuntimeConfigurationProvider(env_file=tmp_path / ".env")
    profile = provider2.get_profile()
    assert profile.require("auth.jwt_secret") == "recovered-secret"
