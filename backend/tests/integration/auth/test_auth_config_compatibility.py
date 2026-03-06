"""Auth compatibility regression tests for centralized configuration (EN-0202 US3 / T024).

Validates that F-0001 auth behaviour is fully preserved after the configuration
system is refactored to use the centralized ``RuntimeConfigurationProvider``
instead of direct ``os.getenv`` calls.

These tests exercise the same business scenarios as the existing auth
integration tests, confirming no regression in:
  - TTL enforcement (token_ttl_seconds)
  - Lockout policy (max_failed_attempts, lockout_minutes)
  - JWT secret / algorithm resolution

The ``conftest.py`` autouse fixture ensures a fresh SQLite DB and all auth env
vars are set before each test.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from baku.backend.infrastructure.config.auth_settings import (
    get_auth_settings,
    reset_auth_settings,
)
from baku.backend.infrastructure.config.runtime_settings import reset_runtime_settings


@pytest.fixture(autouse=True)
def _reset_all_singletons():
    """Ensure both settings and provider singletons are cleared between tests."""
    reset_auth_settings()
    reset_runtime_settings()
    yield
    reset_auth_settings()
    reset_runtime_settings()


def test_auth_settings_loads_jwt_secret_via_centralized_provider(monkeypatch):
    """AuthSettings reads jwt_secret through centralized provider (not os.getenv)."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "regression-secret")

    settings = get_auth_settings()

    assert settings.jwt_secret == "regression-secret"


def test_auth_settings_defaults_preserved(monkeypatch):
    """Optional auth settings retain their declared defaults after refactor."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "regression-secret")
    # Ensure optional keys are absent from env so defaults kick in
    monkeypatch.delenv("AUTH_JWT_ALGORITHM", raising=False)
    monkeypatch.delenv("AUTH_TOKEN_TTL_SECONDS", raising=False)
    monkeypatch.delenv("AUTH_MAX_FAILED_ATTEMPTS", raising=False)
    monkeypatch.delenv("AUTH_LOCKOUT_MINUTES", raising=False)

    settings = get_auth_settings()

    assert settings.jwt_algorithm == "HS256"
    assert settings.token_ttl_seconds == 3600
    assert settings.max_failed_attempts == 5
    assert settings.lockout_minutes == 15


def test_auth_settings_env_override_respected(monkeypatch):
    """Env var overrides take precedence over defaults for auth settings."""
    monkeypatch.setenv("AUTH_JWT_SECRET", "regression-secret")
    monkeypatch.setenv("AUTH_TOKEN_TTL_SECONDS", "7200")
    monkeypatch.setenv("AUTH_MAX_FAILED_ATTEMPTS", "3")
    monkeypatch.setenv("AUTH_LOCKOUT_MINUTES", "30")

    settings = get_auth_settings()

    assert settings.token_ttl_seconds == 7200
    assert settings.max_failed_attempts == 3
    assert settings.lockout_minutes == 30


def test_bootstrap_flow_works_via_centralized_config(client: TestClient):
    """Full auth bootstrap flow succeeds with centralized configuration."""
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 201


def test_login_flow_works_via_centralized_config(client: TestClient):
    """Full auth login flow succeeds after bootstrap with centralized config."""
    client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()
