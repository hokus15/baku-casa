"""Contract tests: POST /api/v1/auth/login, POST /api/v1/auth/logout.

Validates OpenAPI contract shape: status codes, response fields and error schema.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

# ── Login ─────────────────────────────────


def test_login_returns_200_with_token(bootstrapped_client: TestClient) -> None:
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "Bearer"
    assert "expires_at" in body


def test_login_returns_401_on_wrong_password(bootstrapped_client: TestClient) -> None:
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong-password"},
    )
    assert resp.status_code == 401


def test_login_401_body_matches_error_schema(bootstrapped_client: TestClient) -> None:
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong-password"},
    )
    body = resp.json()
    assert body["error_code"] == "AUTH_INVALID_CREDENTIALS"
    assert "message" in body
    assert "correlation_id" in body


def test_login_returns_429_after_max_failed_attempts(bootstrapped_client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("AUTH_MAX_FAILED_ATTEMPTS", "3")
    from baku.backend.infrastructure.config.auth_settings import reset_auth_settings

    reset_auth_settings()

    for _ in range(3):
        bootstrapped_client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "wrong"},
        )

    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert resp.status_code == 429
    assert resp.json()["error_code"] == "AUTH_LOCKED_TEMPORARILY"


# ── Logout ─────────────────────────────────────────────────────────────────────


def test_logout_returns_204(bootstrapped_client: TestClient, auth_token: str) -> None:
    resp = bootstrapped_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 204


def test_logout_without_token_returns_401_with_error_schema(
    bootstrapped_client: TestClient,
) -> None:
    resp = bootstrapped_client.post("/api/v1/auth/logout")
    assert resp.status_code == 401
    body = resp.json()
    assert body["error_code"] == "AUTH_TOKEN_INVALID"
    assert "message" in body
    assert "correlation_id" in body
