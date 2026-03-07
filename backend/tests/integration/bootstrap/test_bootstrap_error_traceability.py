"""Integration test: bootstrap error traceability (US3, T037).

Verifies that error responses produced through the modularized bootstrap
include structured correlation evidence consistent with ADR-0009 and the
error model (correlation_id, error_code, message).

Spec: FR-009 — bootstrap error traceability with structured correlation evidence.
ADR-0009 — all error responses must include correlation_id and stable error_code.
Constitution §III — error response contract.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_domain_error_response_includes_correlation_id(client: TestClient) -> None:
    """Domain error responses must include correlation_id (ADR-0009, constitution §III)."""
    # Trigger a domain error: second bootstrap attempt produces AUTH_BOOTSTRAP_ALREADY_COMPLETED
    client.post("/api/v1/auth/bootstrap", json={"username": "admin", "password": "secure-pass-1"})
    resp = client.post("/api/v1/auth/bootstrap", json={"username": "other", "password": "other-pass-1"})

    assert resp.status_code == 409
    body = resp.json()
    assert "correlation_id" in body, "Error response must include 'correlation_id' field"
    assert body["correlation_id"], "correlation_id must be non-empty"


def test_domain_error_response_includes_error_code(client: TestClient) -> None:
    """Domain error responses must include a stable error_code (ADR-0009)."""
    client.post("/api/v1/auth/bootstrap", json={"username": "admin", "password": "secure-pass-1"})
    resp = client.post("/api/v1/auth/bootstrap", json={"username": "other", "password": "other-pass-1"})

    assert resp.status_code == 409
    body = resp.json()
    assert "error_code" in body, "Error response must include 'error_code' field"
    assert body["error_code"] == "AUTH_BOOTSTRAP_ALREADY_COMPLETED"


def test_domain_error_response_includes_message(client: TestClient) -> None:
    """Domain error responses must include a 'message' field (constitution error model)."""
    client.post("/api/v1/auth/bootstrap", json={"username": "admin", "password": "secure-pass-1"})
    resp = client.post("/api/v1/auth/bootstrap", json={"username": "other", "password": "other-pass-1"})

    assert resp.status_code == 409
    body = resp.json()
    assert "message" in body, "Error response must include 'message' field"
    assert body["message"], "message must be non-empty"


def test_structured_error_model_on_auth_failure(client: TestClient) -> None:
    """Failed login must respond with full structured error model (all traceability fields)."""
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "wrong-pass-1"},
    )
    assert resp.status_code == 401
    body = resp.json()
    assert "error_code" in body, "error_code missing from auth failure response"
    assert "message" in body, "message missing from auth failure response"
    assert "correlation_id" in body, "correlation_id missing from auth failure response"
    assert body["correlation_id"], "correlation_id must be non-empty"


def test_correlation_id_header_propagated_to_response(client: TestClient) -> None:
    """When X-Correlation-ID header is sent, the same value must appear in the error body."""
    sentinel_id = "test-trace-abc123"
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "wrong-pass-1"},
        headers={"X-Correlation-ID": sentinel_id},
    )
    assert resp.status_code == 401
    body = resp.json()
    assert (
        body.get("correlation_id") == sentinel_id
    ), f"Expected correlation_id={sentinel_id!r}, got {body.get('correlation_id')!r}"
