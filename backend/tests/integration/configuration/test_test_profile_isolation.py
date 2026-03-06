"""Integration test: test-profile isolation (EN-0202 US3).

Verifies that the centralized configuration system is fully isolated between
tests via ``reset_runtime_settings()``, ensuring test reproducibility.
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


def test_env_change_between_tests_is_isolated_first(monkeypatch):
    """First test sets AUTH_JWT_SECRET; profile resolves successfully."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "test-isolation-secret-1")

    provider = RuntimeConfigurationProvider(env_file=None)
    profile = provider.get_profile()

    assert profile.require("auth.jwt_secret") == "test-isolation-secret-1"


def test_env_change_between_tests_is_isolated_second(monkeypatch):
    """Second test uses a different secret; singleton is cleared between tests."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "test-isolation-secret-2")

    provider = RuntimeConfigurationProvider(env_file=None)
    profile = provider.get_profile()

    assert profile.require("auth.jwt_secret") == "test-isolation-secret-2"


def test_reset_clears_cached_profile(monkeypatch):
    """After reset, a new provider instance re-resolves the profile."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "initial-secret")

    provider = RuntimeConfigurationProvider(env_file=None)
    first_profile = provider.get_profile()

    reset_runtime_settings()
    monkeypatch.setenv("AUTH_JWT_SECRET", "updated-secret")

    provider2 = RuntimeConfigurationProvider(env_file=None)
    second_profile = provider2.get_profile()

    assert first_profile.require("auth.jwt_secret") == "initial-secret"
    assert second_profile.require("auth.jwt_secret") == "updated-secret"


def test_absent_secret_after_reset_fails_cleanly(monkeypatch, tmp_path):
    """After reset, absent required key raises without leaking prior state.

    An explicit env_file that doesn't exist ensures the file source is empty,
    so only env vars are consulted.
    """
    monkeypatch.setenv("AUTH_JWT_SECRET", "some-secret")

    provider = RuntimeConfigurationProvider(env_file=tmp_path / ".env")
    provider.get_profile()  # warm the cache

    reset_runtime_settings()
    monkeypatch.delenv("AUTH_JWT_SECRET", raising=False)

    provider2 = RuntimeConfigurationProvider(env_file=tmp_path / ".env")
    with pytest.raises(AggregatedConfigurationError):
        provider2.get_profile()
