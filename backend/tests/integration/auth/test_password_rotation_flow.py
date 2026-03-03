"""Integration tests: password rotation with global token revocation (US3).

Verifies that credential_version increment invalidates all prior tokens (FR-007, FR-008).
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_password_change_succeeds(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    resp = bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "secure-pass-1", "new_password": "new-secure-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 204


def test_prior_token_revoked_after_password_change(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    """Tokens issued before password change are revoked globally via credential_version."""
    bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "secure-pass-1", "new_password": "new-secure-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    # Try to use old token
    resp = bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "new-secure-pass-2", "new_password": "another-pass-3"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 401
    assert resp.json()["error_code"] == "AUTH_TOKEN_REVOKED"


def test_new_credentials_allow_fresh_login_after_rotation(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "secure-pass-1", "new_password": "new-secure-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    # Login with new password must succeed
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "new-secure-pass-2"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_old_credentials_rejected_after_rotation(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "secure-pass-1", "new_password": "new-secure-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 401


def test_wrong_current_password_rejected(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    resp = bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "wrong-current", "new_password": "new-secure-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 401
    assert resp.json()["error_code"] == "AUTH_INVALID_CREDENTIALS"


def test_password_change_error_includes_correlation_id(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    resp = bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "wrong", "new_password": "new-secure-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert "correlation_id" in resp.json()
