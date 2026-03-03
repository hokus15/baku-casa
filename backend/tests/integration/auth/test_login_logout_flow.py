"""Integration tests: login/logout flow with revocation (US2).

Includes edge case: double logout idempotency.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_valid_login_returns_token(bootstrapped_client: TestClient) -> None:
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["access_token"]
    assert body["token_type"] == "Bearer"
    assert "expires_at" in body


def test_invalid_credentials_rejected(bootstrapped_client: TestClient) -> None:
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong-password"},
    )
    assert resp.status_code == 401
    assert resp.json()["error_code"] == "AUTH_INVALID_CREDENTIALS"


def test_missing_credentials_rejected(bootstrapped_client: TestClient) -> None:
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "pass"},
    )
    assert resp.status_code == 401


def test_logout_revokes_token(bootstrapped_client: TestClient, auth_token: str) -> None:
    # Logout
    resp = bootstrapped_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 204

    # Attempt reuse of revoked token
    resp2 = bootstrapped_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    # Second logout with same (now revoked) token: token is revoked → 401
    assert resp2.status_code == 401
    assert resp2.json()["error_code"] == "AUTH_TOKEN_REVOKED"


def test_double_logout_is_rejected_with_401(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    """Edge case: double logout — second call must return 401 TOKEN_REVOKED (idempotent DB,
    non-idempotent HTTP contract per design: token is already invalid on second use)."""
    bootstrapped_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = bootstrapped_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 401
    assert resp.json()["error_code"] == "AUTH_TOKEN_REVOKED"


def test_revoked_token_cannot_access_protected_route(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    bootstrapped_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    # PUT /api/v1/auth/password is a protected route
    resp = bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "secure-pass-1", "new_password": "new-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 401


def test_error_responses_include_correlation_id(bootstrapped_client: TestClient) -> None:
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert "correlation_id" in resp.json()
