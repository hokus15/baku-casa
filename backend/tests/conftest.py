"""Shared test fixtures for auth integration and contract tests."""

from __future__ import annotations

from collections.abc import Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from baku.backend.infrastructure.config.auth_settings import reset_auth_settings
from baku.backend.infrastructure.config.pagination_settings import reset_pagination_settings
from baku.backend.infrastructure.config.runtime_settings import reset_runtime_settings
from baku.backend.infrastructure.persistence.sqlite.db import reset_engine
from baku.backend.infrastructure.persistence.sqlite.migrations import upgrade_to_head
from baku.backend.main import app


def _build_inmemory_db_url() -> str:
    """Return a named shared in-memory SQLite URL for a single test case."""
    return f"sqlite+pysqlite:///file:baku_test_{uuid4().hex}?mode=memory&cache=shared&uri=true"


@pytest.fixture()
def test_db_url() -> str:
    """Expose the active test DB URL for integration assertions."""
    return _build_inmemory_db_url()


@pytest.fixture(autouse=True)
def _reset_singletons(test_db_url: str, monkeypatch):
    """Isolate each test with a unique, freshly migrated in-memory SQLite DB."""
    db_url = test_db_url
    monkeypatch.setenv("TEST_DATABASE_URL", db_url)
    monkeypatch.setenv("DATABASE_URL", db_url)
    monkeypatch.setenv("AUTH_JWT_SECRET", "test-secret-key-for-testing-only")
    monkeypatch.setenv("AUTH_TOKEN_TTL_SECONDS", "3600")
    monkeypatch.setenv("AUTH_MAX_FAILED_ATTEMPTS", "5")
    monkeypatch.setenv("AUTH_LOCKOUT_MINUTES", "15")

    reset_engine()
    reset_auth_settings()
    reset_pagination_settings()
    reset_runtime_settings()
    upgrade_to_head(db_url)

    yield

    reset_engine()
    reset_auth_settings()
    reset_pagination_settings()
    reset_runtime_settings()


@pytest.fixture()
def client(_reset_singletons: None) -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


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
