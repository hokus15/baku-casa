"""Contract tests: DELETE /api/v1/owners/{owner_id}."""

from __future__ import annotations

from fastapi.testclient import TestClient

_VALID_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "María",
    "last_name": "García",
    "legal_name": "María García",
    "tax_id": "99999999R",
    "fiscal_address_line1": "Plaza España 3",
    "fiscal_address_city": "Sevilla",
    "fiscal_address_postal_code": "41001",
}


def _create_owner(client: TestClient, token: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def test_delete_owner_returns_204(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    resp = client.delete(
        f"/api/v1/owners/{owner_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 204


def test_delete_owner_returns_404_for_unknown(auth_token: str, client: TestClient) -> None:
    resp = client.delete(
        "/api/v1/owners/nonexistent-id",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_delete_owner_returns_404_on_second_delete(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    client.delete(
        f"/api/v1/owners/{owner_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = client.delete(
        f"/api/v1/owners/{owner_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_delete_owner_returns_401_without_auth(client: TestClient) -> None:
    resp = client.delete("/api/v1/owners/some-id")
    assert resp.status_code == 401
