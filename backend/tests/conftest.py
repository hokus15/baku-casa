"""Shared test fixtures for auth integration and contract tests."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from baku.backend.infrastructure.config.auth_settings import reset_auth_settings
from baku.backend.infrastructure.persistence.sqlite.db import reset_engine
from baku.backend.main import app


@pytest.fixture(autouse=True)
def _reset_singletons(tmp_path, monkeypatch):
    """Isolate each test with a fresh in-memory SQLite DB and auth settings."""
    db_url = "sqlite://"  # in-memory
    monkeypatch.setenv("DATABASE_URL", db_url)
    monkeypatch.setenv("AUTH_JWT_SECRET", "test-secret-key-for-testing-only")
    monkeypatch.setenv("AUTH_TOKEN_TTL_SECONDS", "3600")
    monkeypatch.setenv("AUTH_MAX_FAILED_ATTEMPTS", "5")
    monkeypatch.setenv("AUTH_LOCKOUT_MINUTES", "15")

    reset_engine()
    reset_auth_settings()

    yield

    reset_engine()
    reset_auth_settings()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture()
def bootstrapped_client(client: TestClient) -> TestClient:
    """Client with operator already bootstrapped."""
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 201
    return client


@pytest.fixture()
def auth_token(bootstrapped_client: TestClient) -> str:
    """Valid JWT for the bootstrapped operator."""
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]
