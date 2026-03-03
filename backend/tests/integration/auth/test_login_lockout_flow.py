"""Integration tests: login lockout / throttle flow (US2).

Verifies configurable brute-force protection (FR-016–FR-019).
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def _exhaust_attempts(client: TestClient, n: int) -> None:
    for _ in range(n):
        client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "wrong-password"},
        )


def test_lockout_activates_after_max_failed_attempts(
    bootstrapped_client: TestClient, monkeypatch
) -> None:
    monkeypatch.setenv("AUTH_MAX_FAILED_ATTEMPTS", "3")
    from baku.backend.infrastructure.config.auth_settings import reset_auth_settings

    reset_auth_settings()

    _exhaust_attempts(bootstrapped_client, 3)

    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong-password"},
    )
    assert resp.status_code == 429
    assert resp.json()["error_code"] == "AUTH_LOCKED_TEMPORARILY"


def test_lockout_rejects_even_correct_credentials(
    bootstrapped_client: TestClient, monkeypatch
) -> None:
    monkeypatch.setenv("AUTH_MAX_FAILED_ATTEMPTS", "3")
    from baku.backend.infrastructure.config.auth_settings import reset_auth_settings

    reset_auth_settings()

    _exhaust_attempts(bootstrapped_client, 3)

    # Even with correct credentials the account is blocked
    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secure-pass-1"},
    )
    assert resp.status_code == 429


def test_lockout_threshold_is_configurable(
    bootstrapped_client: TestClient, monkeypatch
) -> None:
    """Verify that changing AUTH_MAX_FAILED_ATTEMPTS changes when lockout activates."""
    monkeypatch.setenv("AUTH_MAX_FAILED_ATTEMPTS", "2")
    from baku.backend.infrastructure.config.auth_settings import reset_auth_settings

    reset_auth_settings()

    _exhaust_attempts(bootstrapped_client, 2)

    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert resp.status_code == 429


def test_lockout_error_includes_correlation_id(
    bootstrapped_client: TestClient, monkeypatch
) -> None:
    monkeypatch.setenv("AUTH_MAX_FAILED_ATTEMPTS", "2")
    from baku.backend.infrastructure.config.auth_settings import reset_auth_settings

    reset_auth_settings()

    _exhaust_attempts(bootstrapped_client, 2)

    resp = bootstrapped_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert "correlation_id" in resp.json()
