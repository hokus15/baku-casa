"""Integration tests: Soft delete owner — US5."""

from __future__ import annotations

from fastapi.testclient import TestClient

_VALID_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Soft Delete",
    "last_name": "Tester",
    "legal_name": "Soft Delete Tester",
    "tax_id": "SDTEST001",
    "fiscal_address_line1": "Calle SD 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}


def _create(client: TestClient, token: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def test_soft_deleted_owner_not_in_default_list(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    owner_id = _create(client, auth_token)
    client.delete(f"/api/v1/owners/{owner_id}", headers=headers)
    body = client.get("/api/v1/owners", headers=headers).json()
    assert body["total"] == 0


def test_soft_deleted_owner_appears_with_include_deleted(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    owner_id = _create(client, auth_token)
    client.delete(f"/api/v1/owners/{owner_id}", headers=headers)
    body = client.get("/api/v1/owners?include_deleted=true", headers=headers).json()
    assert body["total"] == 1
    assert body["items"][0]["deleted_at"] is not None


def test_soft_delete_sets_deleted_by(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    owner_id = _create(client, auth_token)
    client.delete(f"/api/v1/owners/{owner_id}", headers=headers)
    body = client.get(f"/api/v1/owners/{owner_id}?include_deleted=true", headers=headers).json()
    assert body["deleted_by"] is not None


def test_delete_again_returns_404(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    owner_id = _create(client, auth_token)
    client.delete(f"/api/v1/owners/{owner_id}", headers=headers)
    resp = client.delete(f"/api/v1/owners/{owner_id}", headers=headers)
    assert resp.status_code == 404
