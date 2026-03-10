"""Contract tests: PATCH /api/v1/properties/{id} and PUT /api/v1/properties/{id}/ownership.

Validates response shape, status codes and error schema against
properties-api-v1.yaml contract (ADR-0006).
Tests execute in RED state until implementation is complete (TDD).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Luis",
    "last_name": "Fernández",
    "legal_name": "Luis Fernández Ruiz",
    "tax_id": "11111111A",
    "fiscal_address_line1": "Paseo Castellana 100",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28046",
}


def _create_owner(client: TestClient, auth_token: str, tax_id: str) -> str:
    payload = {**_OWNER_PAYLOAD, "tax_id": tax_id}
    resp = client.post(
        "/api/v1/owners",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def _create_property(
    client: TestClient, auth_token: str, owner_id: str, name: str = "Piso Test"
) -> str:
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": name,
            "type": "VIVIENDA",
            "ownerships": [
                {"owner_id": owner_id, "ownership_percentage": "100.00"}
            ],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["property_id"]


# ---------------------------------------------------------------------------
# PATCH /api/v1/properties/{property_id}
# ---------------------------------------------------------------------------


def test_patch_property_returns_200(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "22222222B")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.patch(
        f"/api/v1/properties/{property_id}",
        json={"name": "Piso Actualizado"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_patch_property_response_reflects_update(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "33333333C")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.patch(
        f"/api/v1/properties/{property_id}",
        json={"name": "Nombre Nuevo", "city": "Barcelona"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["name"] == "Nombre Nuevo"
    assert body["city"] == "Barcelona"


def test_patch_property_returns_404_for_unknown_id(
    auth_token: str, client: TestClient
) -> None:
    resp = client.patch(
        "/api/v1/properties/does-not-exist",
        json={"name": "X"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_patch_property_returns_401_without_auth(client: TestClient) -> None:
    resp = client.patch(
        "/api/v1/properties/some-id",
        json={"name": "X"},
    )
    assert resp.status_code == 401


def test_patch_property_rejects_empty_name(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "44444444D")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.patch(
        f"/api/v1/properties/{property_id}",
        json={"name": ""},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# PUT /api/v1/properties/{property_id}/ownership
# ---------------------------------------------------------------------------


def test_put_ownership_returns_200(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "55555555E")
    owner_b = _create_owner(client, auth_token, "66666666F")
    property_id = _create_property(client, auth_token, owner_a)
    resp = client.put(
        f"/api/v1/properties/{property_id}/ownership",
        json={
            "ownerships": [
                {"owner_id": owner_b, "ownership_percentage": "100.00"}
            ]
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_put_ownership_response_reflects_new_owners(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "77777777G")
    owner_b = _create_owner(client, auth_token, "88888888H")
    property_id = _create_property(client, auth_token, owner_a)
    resp = client.put(
        f"/api/v1/properties/{property_id}/ownership",
        json={
            "ownerships": [
                {"owner_id": owner_b, "ownership_percentage": "50.00"},
                {"owner_id": owner_a, "ownership_percentage": "50.00"},
            ]
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    owner_ids = [o["owner_id"] for o in body["ownerships"]]
    assert owner_a in owner_ids
    assert owner_b in owner_ids


def test_put_ownership_returns_409_when_sum_exceeds_100(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "11112222A")
    owner_b = _create_owner(client, auth_token, "22223333B")
    property_id = _create_property(client, auth_token, owner_a)
    resp = client.put(
        f"/api/v1/properties/{property_id}/ownership",
        json={
            "ownerships": [
                {"owner_id": owner_a, "ownership_percentage": "60.00"},
                {"owner_id": owner_b, "ownership_percentage": "60.00"},
            ]
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 409


def test_put_ownership_returns_400_for_empty_ownerships(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "33334444C")
    property_id = _create_property(client, auth_token, owner_a)
    resp = client.put(
        f"/api/v1/properties/{property_id}/ownership",
        json={"ownerships": []},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400


def test_put_ownership_returns_404_for_unknown_property(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "44445555D")
    resp = client.put(
        "/api/v1/properties/does-not-exist/ownership",
        json={
            "ownerships": [
                {"owner_id": owner_a, "ownership_percentage": "100.00"}
            ]
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_put_ownership_returns_401_without_auth(client: TestClient) -> None:
    resp = client.put(
        "/api/v1/properties/some-id/ownership",
        json={
            "ownerships": [{"owner_id": "x", "ownership_percentage": "100.00"}]
        },
    )
    assert resp.status_code == 401
