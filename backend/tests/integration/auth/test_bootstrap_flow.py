"""Integration tests: bootstrap flow (US1).

Verifies bootstrap business rules with a real SQLite in-memory DB.
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_bootstrap_creates_operator_successfully(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 201


def test_second_bootstrap_is_rejected(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "other", "password": "other-pass-1"},
    )
    assert resp.status_code == 409
    assert resp.json()["error_code"] == "AUTH_BOOTSTRAP_ALREADY_COMPLETED"


def test_after_bootstrap_login_is_possible(client: TestClient) -> None:
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


def test_bootstrap_response_includes_correlation_id_on_conflict(
    client: TestClient,
) -> None:
    client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert "correlation_id" in resp.json()
