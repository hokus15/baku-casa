"""Contract tests: GET /api/v1/owners/{owner_id}."""

from __future__ import annotations

from fastapi.testclient import TestClient

_VALID_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Ana",
    "last_name": "Martínez",
    "legal_name": "Ana Martínez",
    "tax_id": "87654321A",
    "fiscal_address_line1": "Paseo del Prado 5",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28014",
}


def _create_owner(client: TestClient, token: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def test_get_owner_detail_returns_200_for_active(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    resp = client.get(
        f"/api/v1/owners/{owner_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_get_owner_detail_response_matches_schema(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    body = client.get(
        f"/api/v1/owners/{owner_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    ).json()
    for field in (
        "owner_id",
        "entity_type",
        "first_name",
        "last_name",
        "legal_name",
        "tax_id",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    ):
        assert field in body


def test_get_owner_detail_returns_404_for_unknown(auth_token: str, client: TestClient) -> None:
    resp = client.get(
        "/api/v1/owners/nonexistent-id",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_get_owner_detail_404_body_matches_error_schema(auth_token: str, client: TestClient) -> None:
    resp = client.get(
        "/api/v1/owners/nonexistent-id",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["error_code"] == "OWNER_NOT_FOUND"
    assert "correlation_id" in body


def test_get_owner_detail_returns_401_without_auth(client: TestClient) -> None:
    resp = client.get("/api/v1/owners/some-id")
    assert resp.status_code == 401


def test_get_owner_detail_null_fields_excluded_from_active_response(auth_token: str, client: TestClient) -> None:
    """Null fields MUST NOT appear in API responses (constitution §API design)."""
    owner_id = _create_owner(client, auth_token)
    body = client.get(
        f"/api/v1/owners/{owner_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    ).json()
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
