"""Integration test: valid startup with required global keys (EN-0202 US1).

Tests that the centralized provider resolves and validates successfully when
all required configuration keys are present.
"""

from __future__ import annotations

import pytest

from baku.backend.application.configuration.models import ResolvedConfigurationProfile
from baku.backend.infrastructure.config.runtime_settings import (
    RuntimeConfigurationProvider,
    reset_runtime_settings,
)


@pytest.fixture(autouse=True)
def _reset_provider():
    """Clear the cached profile before and after each test."""
    reset_runtime_settings()
    yield
    reset_runtime_settings()


def test_provider_returns_profile_when_required_keys_present(monkeypatch):
    """Provider resolves successfully with all required keys in env."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "super-secret-value")

    provider = RuntimeConfigurationProvider(env_file=None)
    profile = provider.get_profile()

    assert isinstance(profile, ResolvedConfigurationProfile)
    assert profile.require("auth.jwt_secret") == "super-secret-value"


def test_profile_contains_defaults_for_optional_keys(monkeypatch):
    """Optional keys fall back to their declared defaults when absent."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "super-secret-value")
    # Do NOT set optional keys; defaults should apply.

    provider = RuntimeConfigurationProvider(env_file=None)
    profile = provider.get_profile()

    assert profile.require("auth.jwt_algorithm") == "HS256"
    assert profile.require("auth.token_ttl_seconds") == "3600"
    assert profile.require("auth.max_failed_attempts") == "5"
    assert profile.require("auth.lockout_minutes") == "15"


def test_provider_is_idempotent(monkeypatch):
    """Calling get_profile() multiple times returns the same object."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "super-secret-value")

    provider = RuntimeConfigurationProvider(env_file=None)
    first = provider.get_profile()
    second = provider.get_profile()

    assert first is second


def test_source_map_shows_env_for_env_sourced_key(monkeypatch):
    """source_map correctly attributes env-sourced keys."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "from-env")

    provider = RuntimeConfigurationProvider(env_file=None)
    profile = provider.get_profile()

    assert profile.source_map.get("auth.jwt_secret") == "env"


def test_source_map_shows_default_for_unset_optional_keys(monkeypatch, tmp_path):
    """source_map correctly attributes default-sourced optional keys.

    Uses a non-existent env_file so that the file source is empty and default
    attribution is observable.
    """
    monkeypatch.setenv("AUTH_JWT_SECRET", "from-env")
    # Do NOT set AUTH_JWT_ALGORITHM in env; use a missing file to avoid file source.
    monkeypatch.delenv("AUTH_JWT_ALGORITHM", raising=False)

    provider = RuntimeConfigurationProvider(env_file=tmp_path / ".env")
    profile = provider.get_profile()

    assert profile.source_map.get("auth.jwt_algorithm") == "default"
