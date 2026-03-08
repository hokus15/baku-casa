"""Integration tests: Create owner flow — US1."""

from __future__ import annotations

from fastapi.testclient import TestClient

_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Test",
    "last_name": "Owner",
    "legal_name": "Test Owner",
    "tax_id": "12345678Z",
    "fiscal_address_line1": "Calle Test 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}


def test_create_owner_persists_and_is_retrievable(auth_token: str, client: TestClient) -> None:
    create_resp = client.post(
        "/api/v1/owners",
        json=_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert create_resp.status_code == 201
    owner_id = create_resp.json()["owner_id"]

    get_resp = client.get(
        f"/api/v1/owners/{owner_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert get_resp.status_code == 200
    assert get_resp.json()["owner_id"] == owner_id


def test_create_owner_default_country_es(auth_token: str, client: TestClient) -> None:
    resp = client.post(
        "/api/v1/owners",
        json=_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.json()["fiscal_address_country"] == "ES"


def test_create_owner_with_explicit_country(auth_token: str, client: TestClient) -> None:
    payload = {**_PAYLOAD, "fiscal_address_country": "PT"}
    resp = client.post(
        "/api/v1/owners",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.json()["fiscal_address_country"] == "PT"


def test_create_owner_audit_fields_are_set(auth_token: str, client: TestClient) -> None:
    resp = client.post(
        "/api/v1/owners",
        json=_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["created_by"] is not None
    assert body["updated_by"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None
    # Null fields must be absent from response (constitution §API design)
    assert "deleted_at" not in body
    assert "deleted_by" not in body


def test_create_owner_conflict_returns_409(auth_token: str, client: TestClient) -> None:
    client.post("/api/v1/owners", json=_PAYLOAD, headers={"Authorization": f"Bearer {auth_token}"})
    resp = client.post("/api/v1/owners", json=_PAYLOAD, headers={"Authorization": f"Bearer {auth_token}"})
    assert resp.status_code == 409
    assert resp.json()["error_code"] == "OWNER_TAX_ID_CONFLICT"
