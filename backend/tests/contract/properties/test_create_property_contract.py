"""Contract tests: POST /api/v1/properties.

Validates response shape, status codes and error schema against
properties-api-v1.yaml contract (ADR-0006).
Tests execute in RED state until implementation is complete (TDD).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

_VALID_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Juan",
    "last_name": "García López",
    "legal_name": "Juan García López",
    "tax_id": "12345678Z",
    "fiscal_address_line1": "Calle Mayor 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}

_VALID_PROPERTY_PAYLOAD = {
    "name": "Piso Calle Mayor 1",
    "type": "VIVIENDA",
    "ownerships": [
        {"owner_id": "__OWNER_ID__", "ownership_percentage": "100.00"},
    ],
}


def _create_owner(client: TestClient, auth_token: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_OWNER_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def test_create_property_returns_201_with_valid_payload(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token)
    payload = {
        **_VALID_PROPERTY_PAYLOAD,
        "ownerships": [
            {"owner_id": owner_id, "ownership_percentage": "100.00"}
        ],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201


def test_create_property_response_has_property_id(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token)
    payload = {
        **_VALID_PROPERTY_PAYLOAD,
        "ownerships": [
            {"owner_id": owner_id, "ownership_percentage": "100.00"}
        ],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert "property_id" in body
    assert len(body["property_id"]) > 0


def test_create_property_response_has_required_fields(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token)
    payload = {
        **_VALID_PROPERTY_PAYLOAD,
        "ownerships": [
            {"owner_id": owner_id, "ownership_percentage": "100.00"}
        ],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    for field in (
        "property_id",
        "name",
        "type",
        "ownerships",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    ):
        assert field in body, f"Missing field: {field}"


def test_create_property_response_excludes_null_optional_fields(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token)
    payload = {
        **_VALID_PROPERTY_PAYLOAD,
        "ownerships": [
            {"owner_id": owner_id, "ownership_percentage": "100.00"}
        ],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    # Optional fields with null value must not appear in the response (constitution §VI)
    for null_field in (
        "description",
        "address",
        "city",
        "deleted_at",
        "deleted_by",
    ):
        assert (
            null_field not in body
        ), f"Null field should be excluded: {null_field}"


def test_create_property_returns_401_without_auth(client: TestClient) -> None:
    resp = client.post("/api/v1/properties", json=_VALID_PROPERTY_PAYLOAD)
    assert resp.status_code == 401


def test_create_property_returns_400_without_name(
    auth_token: str, client: TestClient
) -> None:
    payload = {
        "type": "VIVIENDA",
        "ownerships": [{"owner_id": "any", "ownership_percentage": "100.00"}],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400


def test_create_property_returns_400_without_ownerships(
    auth_token: str, client: TestClient
) -> None:
    payload = {"name": "Test", "type": "VIVIENDA", "ownerships": []}
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400


def test_create_property_returns_404_owner_not_found(
    auth_token: str, client: TestClient
) -> None:
    payload = {
        "name": "Test",
        "type": "VIVIENDA",
        "ownerships": [
            {
                "owner_id": "non-existent-owner-id",
                "ownership_percentage": "100.00",
            }
        ],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404
    body = resp.json()
    assert body["error_code"] == "OWNER_NOT_FOUND"
    assert "correlation_id" in body


def test_create_property_returns_409_ownership_sum_exceeded(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token)
    payload = {
        "name": "Test",
        "type": "VIVIENDA",
        "ownerships": [
            {"owner_id": owner_id, "ownership_percentage": "101.00"}
        ],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 409
    body = resp.json()
    assert body["error_code"] == "PROPERTY_OWNERSHIP_SUM_EXCEEDED"


def test_create_property_returns_400_percentage_precision_exceeded(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token)
    payload = {
        "name": "Test",
        "type": "VIVIENDA",
        "ownerships": [
            {"owner_id": owner_id, "ownership_percentage": "50.123"}
        ],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400


def test_create_property_error_response_has_correlation_id(
    auth_token: str, client: TestClient
) -> None:
    payload = {"type": "VIVIENDA", "ownerships": []}
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400
    body = resp.json()
    assert "correlation_id" in body
    assert "error_code" in body
    assert "message" in body
