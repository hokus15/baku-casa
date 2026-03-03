"""Contract tests: PUT /api/v1/auth/password.

Validates response shape against auth-api-v1.yaml contract.
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_password_change_returns_204(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    resp = bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "secure-pass-1", "new_password": "new-secure-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 204


def test_password_change_without_token_returns_403_or_401(
    bootstrapped_client: TestClient,
) -> None:
    resp = bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "secure-pass-1", "new_password": "new-secure-pass-2"},
    )
    assert resp.status_code in (401, 403)


def test_password_change_wrong_current_returns_401(
    bootstrapped_client: TestClient, auth_token: str
) -> None:
    resp = bootstrapped_client.put(
        "/api/v1/auth/password",
        json={"current_password": "wrong-current", "new_password": "new-secure-pass-2"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 401
    body = resp.json()
    assert "error_code" in body
    assert "message" in body
    assert "correlation_id" in body
