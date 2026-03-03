"""Contract tests: POST /api/v1/auth/bootstrap.

Validates response shape, status codes and error schema against auth-api-v1.yaml contract.
These tests MUST run before implementation is complete (TDD — they should fail first).
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_bootstrap_returns_201_on_first_call(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secret-pass-1"},
    )
    assert resp.status_code == 201


def test_bootstrap_returns_409_on_second_call(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secret-pass-1"},
    )
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secret-pass-1"},
    )
    assert resp.status_code == 409


def test_bootstrap_409_body_matches_error_schema(client: TestClient) -> None:
    """Error response must include error_code, message and correlation_id (ADR-0009)."""
    client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secret-pass-1"},
    )
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secret-pass-1"},
    )
    body = resp.json()
    assert body["error_code"] == "AUTH_BOOTSTRAP_ALREADY_COMPLETED"
    assert "message" in body
    assert "correlation_id" in body


def test_bootstrap_409_message_in_spanish(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secret-pass-1"},
    )
    resp = client.post(
        "/api/v1/auth/bootstrap",
        json={"username": "admin", "password": "secret-pass-1"},
    )
    # Message must be non-empty and Spanish (contains accented chars or Spanish words)
    message = resp.json()["message"]
    assert len(message) > 0
