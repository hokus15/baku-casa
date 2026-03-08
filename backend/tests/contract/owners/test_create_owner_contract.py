"""Contract tests: POST /api/v1/owners.

Validates response shape, status codes and error schema against
owners-api-v1.yaml contract (ADR-0006).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

_VALID_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Juan",
    "last_name": "García López",
    "legal_name": "Juan García López",
    "tax_id": "12345678Z",
    "fiscal_address_line1": "Calle Mayor 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}


def test_create_owner_returns_201_with_valid_payload(auth_token: str, client: TestClient) -> None:
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201


def test_create_owner_response_has_owner_id(auth_token: str, client: TestClient) -> None:
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert "owner_id" in body
    assert len(body["owner_id"]) > 0


def test_create_owner_response_has_required_fields(auth_token: str, client: TestClient) -> None:
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    for field in (
        "owner_id",
        "entity_type",
        "first_name",
        "last_name",
        "legal_name",
        "tax_id",
        "fiscal_address_line1",
        "fiscal_address_city",
        "fiscal_address_postal_code",
        "fiscal_address_country",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    ):
        assert field in body, f"Missing field: {field}"


def test_create_owner_tax_id_is_normalized(auth_token: str, client: TestClient) -> None:
    payload = {**_VALID_PAYLOAD, "tax_id": " 12 345 678-z "}
    resp = client.post(
        "/api/v1/owners",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    assert resp.json()["tax_id"] == "12345678Z"


def test_create_owner_returns_409_on_duplicate_tax_id(auth_token: str, client: TestClient) -> None:
    client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 409


def test_create_owner_409_body_matches_error_schema(auth_token: str, client: TestClient) -> None:
    client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["error_code"] == "OWNER_TAX_ID_CONFLICT"
    assert "message" in body
    assert "correlation_id" in body


def test_create_owner_returns_401_without_auth(client: TestClient) -> None:
    resp = client.post("/api/v1/owners", json=_VALID_PAYLOAD)
    assert resp.status_code == 401


def test_create_owner_returns_400_with_missing_required_field(auth_token: str, client: TestClient) -> None:
    payload = {k: v for k, v in _VALID_PAYLOAD.items() if k != "legal_name"}
    resp = client.post(
        "/api/v1/owners",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400


def test_create_owner_default_country_is_ES(auth_token: str, client: TestClient) -> None:
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.json()["fiscal_address_country"] == "ES"


def test_create_owner_null_fields_excluded_from_response(auth_token: str, client: TestClient) -> None:
    """Null fields MUST NOT appear in API responses (constitution §API design)."""
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    for null_field in (
        "email",
        "land_line",
        "land_line_country_code",
        "mobile",
        "mobile_country_code",
        "stamp_image",
        "deleted_at",
        "deleted_by",
    ):
        assert null_field not in body, f"Null field '{null_field}' must not appear in response"
