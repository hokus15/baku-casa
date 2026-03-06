"""Integration test: deterministic precedence resolution (EN-0202 US1).

Tests that env > file > default precedence is respected when values come from
multiple sources simultaneously.
"""

from __future__ import annotations

import pytest

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


def test_env_overrides_default_for_optional_key(monkeypatch):
    """Env-sourced value wins over built-in default for optional keys."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "my-secret")
    monkeypatch.setenv("AUTH_JWT_ALGORITHM", "RS256")  # default is HS256

    provider = RuntimeConfigurationProvider(env_file=None)
    profile = provider.get_profile()

    assert profile.require("auth.jwt_algorithm") == "RS256"
    assert profile.source_map.get("auth.jwt_algorithm") == "env"


def test_env_overrides_file_for_required_key(monkeypatch, tmp_path):
    """Env-sourced value wins over .env file value for required key."""
    env_file = tmp_path / ".env"
    env_file.write_text("AUTH_JWT_SECRET=from-file\n")

    monkeypatch.setenv("AUTH_JWT_SECRET", "from-env")

    provider = RuntimeConfigurationProvider(env_file=env_file)
    profile = provider.get_profile()

    assert profile.require("auth.jwt_secret") == "from-env"
    assert profile.source_map.get("auth.jwt_secret") == "env"


def test_file_overrides_default_for_optional_key(monkeypatch, tmp_path):
    """File-sourced value wins over default when env var is absent."""
    env_file = tmp_path / ".env"
    env_file.write_text("AUTH_JWT_SECRET=file-secret\nAUTH_JWT_ALGORITHM=HS512\n")

    # Ensure the env var is absent so file takes precedence over default
    monkeypatch.delenv("AUTH_JWT_ALGORITHM", raising=False)
    monkeypatch.delenv("AUTH_JWT_SECRET", raising=False)

    provider = RuntimeConfigurationProvider(env_file=env_file)
    profile = provider.get_profile()

    assert profile.require("auth.jwt_algorithm") == "HS512"
    assert profile.source_map.get("auth.jwt_algorithm") == "file"


def test_default_used_when_key_absent_from_env_and_file(monkeypatch, tmp_path):
    """Default used when key is absent from both env and file."""
    env_file = tmp_path / ".env"
    env_file.write_text("AUTH_JWT_SECRET=file-secret\n")

    monkeypatch.delenv("AUTH_JWT_ALGORITHM", raising=False)
    monkeypatch.delenv("AUTH_JWT_SECRET", raising=False)

    provider = RuntimeConfigurationProvider(env_file=env_file)
    profile = provider.get_profile()

    assert profile.require("auth.jwt_algorithm") == "HS256"
    assert profile.source_map.get("auth.jwt_algorithm") == "default"


def test_all_three_sources_present_env_wins(monkeypatch, tmp_path):
    """When all three sources provide a value, env always wins."""
    env_file = tmp_path / ".env"
    env_file.write_text("AUTH_JWT_SECRET=file-secret\nAUTH_TOKEN_TTL_SECONDS=999\n")

    monkeypatch.setenv("AUTH_JWT_SECRET", "env-secret")
    monkeypatch.setenv("AUTH_TOKEN_TTL_SECONDS", "7200")  # env > file(999) > default(3600)

    provider = RuntimeConfigurationProvider(env_file=env_file)
    profile = provider.get_profile()

    assert profile.require("auth.jwt_secret") == "env-secret"
    assert profile.require("auth.token_ttl_seconds") == "7200"
    assert profile.source_map.get("auth.token_ttl_seconds") == "env"
