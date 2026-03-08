"""Contract tests: PATCH /api/v1/owners/{owner_id}."""

from __future__ import annotations

from fastapi.testclient import TestClient

_PAYLOAD_A = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Pedro",
    "last_name": "Sánchez",
    "legal_name": "Pedro Sánchez",
    "tax_id": "11111111H",
    "fiscal_address_line1": "Calle A 1",
    "fiscal_address_city": "Barcelona",
    "fiscal_address_postal_code": "08001",
}
_PAYLOAD_B = {**_PAYLOAD_A, "legal_name": "Carlos López", "tax_id": "22222222J"}


def _create_owner(client: TestClient, token: str, payload: dict) -> str:
    resp = client.post(
        "/api/v1/owners",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def test_update_owner_returns_200(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token, _PAYLOAD_A)
    resp = client.patch(
        f"/api/v1/owners/{owner_id}",
        json={"legal_name": "Nombre Actualizado"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_update_owner_response_has_updated_field(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token, _PAYLOAD_A)
    resp = client.patch(
        f"/api/v1/owners/{owner_id}",
        json={"legal_name": "Nombre Actualizado"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.json()["legal_name"] == "Nombre Actualizado"


def test_update_owner_returns_404_for_unknown(auth_token: str, client: TestClient) -> None:
    resp = client.patch(
        "/api/v1/owners/nonexistent-id",
        json={"legal_name": "Nuevo"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_update_owner_returns_409_on_tax_id_conflict(auth_token: str, client: TestClient) -> None:
    owner_a = _create_owner(client, auth_token, _PAYLOAD_A)
    _create_owner(client, auth_token, _PAYLOAD_B)
    # Try to update owner_a with owner_b's tax_id
    resp = client.patch(
        f"/api/v1/owners/{owner_a}",
        json={"tax_id": "22222222J"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 409


def test_update_owner_returns_401_without_auth(client: TestClient) -> None:
    resp = client.patch("/api/v1/owners/some-id", json={"legal_name": "X"})
    assert resp.status_code == 401
