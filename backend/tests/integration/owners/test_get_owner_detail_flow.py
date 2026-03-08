"""Integration tests: GET /api/v1/owners/{owner_id} — include_deleted — US2."""

from __future__ import annotations

from fastapi.testclient import TestClient

_VALID_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Detail Test",
    "last_name": "Owner",
    "legal_name": "Detail Test Owner",
    "tax_id": "55555555K",
    "fiscal_address_line1": "Avenida Test 5",
    "fiscal_address_city": "Valencia",
    "fiscal_address_postal_code": "46001",
}


def _create_and_delete(client: TestClient, token: str) -> str:
    create = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    owner_id = create.json()["owner_id"]
    client.delete(f"/api/v1/owners/{owner_id}", headers={"Authorization": f"Bearer {token}"})
    return owner_id


def test_get_detail_returns_404_for_deleted_without_flag(auth_token: str, client: TestClient) -> None:
    owner_id = _create_and_delete(client, auth_token)
    resp = client.get(f"/api/v1/owners/{owner_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert resp.status_code == 404


def test_get_detail_returns_200_for_deleted_with_flag(auth_token: str, client: TestClient) -> None:
    owner_id = _create_and_delete(client, auth_token)
    resp = client.get(
        f"/api/v1/owners/{owner_id}?include_deleted=true",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["deleted_at"] is not None
    assert body["deleted_by"] is not None


def test_get_detail_active_owner_deleted_at_is_null(auth_token: str, client: TestClient) -> None:
    create = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    owner_id = create.json()["owner_id"]
    resp = client.get(f"/api/v1/owners/{owner_id}", headers={"Authorization": f"Bearer {auth_token}"})
    # Null fields must be absent from response (constitution §API design)
    assert "deleted_at" not in resp.json()
    assert "deleted_by" not in resp.json()
