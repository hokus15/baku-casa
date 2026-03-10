"""Integration tests: update property and ownership invariants — F-0003 US3.

Tests verify PATCH update semantics, ownership replacement invariants,
sum validation, and business rules.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_owner(client: TestClient, auth_token: str, tax_id: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json={
            "entity_type": "PERSONA_FISICA",
            "first_name": "Carla",
            "last_name": "Vega",
            "legal_name": "Carla Vega",
            "tax_id": tax_id,
            "fiscal_address_line1": "Paseo de Gracia 40",
            "fiscal_address_city": "Barcelona",
            "fiscal_address_postal_code": "08007",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def _create_property(
    client: TestClient,
    auth_token: str,
    owner_id: str,
    name: str = "Piso Test",
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
# PATCH semantics
# ---------------------------------------------------------------------------


def test_patch_only_updates_provided_fields(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "U1111111A")
    property_id = _create_property(
        client, auth_token, owner_id, "Piso Original"
    )
    resp = client.patch(
        f"/api/v1/properties/{property_id}",
        json={"city": "Zaragoza"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["name"] == "Piso Original"
    assert body["city"] == "Zaragoza"


def test_patch_updates_updated_at_timestamp(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "U2222222B")
    property_id = _create_property(client, auth_token, owner_id)

    created_resp = client.get(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    original_updated_at = created_resp.json()["updated_at"]

    import time

    time.sleep(0.01)

    client.patch(
        f"/api/v1/properties/{property_id}",
        json={"city": "Valencia"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp2 = client.get(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp2.json()["updated_at"] >= original_updated_at


def test_patch_multiple_fields_at_once(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "U3333333C")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.patch(
        f"/api/v1/properties/{property_id}",
        json={
            "name": "Nuevo Nombre",
            "type": "APARTAMENTO",
            "address": "Calle Nueva 1",
            "city": "Bilbao",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["name"] == "Nuevo Nombre"
    assert body["type"] == "APARTAMENTO"
    assert body["city"] == "Bilbao"


# ---------------------------------------------------------------------------
# Ownership replacement invariants
# ---------------------------------------------------------------------------


def test_put_ownership_replaces_all_previous_owners(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "U4444444D")
    owner_b = _create_owner(client, auth_token, "U5555555E")
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
    body = resp.json()
    owner_ids = [o["owner_id"] for o in body["ownerships"]]
    assert owner_b in owner_ids
    assert owner_a not in owner_ids


def test_put_ownership_rejects_duplicate_owners_in_same_request(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "U6666666F")
    property_id = _create_property(client, auth_token, owner_a)

    resp = client.put(
        f"/api/v1/properties/{property_id}/ownership",
        json={
            "ownerships": [
                {"owner_id": owner_a, "ownership_percentage": "50.00"},
                {"owner_id": owner_a, "ownership_percentage": "50.00"},
            ]
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 409


def test_put_ownership_rejects_percentage_with_excess_decimals(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "U7777777G")
    property_id = _create_property(client, auth_token, owner_a)

    resp = client.put(
        f"/api/v1/properties/{property_id}/ownership",
        json={
            "ownerships": [
                {"owner_id": owner_a, "ownership_percentage": "33.333"}
            ]
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400


def test_put_ownership_allows_partial_sum(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "U8888888H")
    owner_b = _create_owner(client, auth_token, "U9999999I")
    property_id = _create_property(client, auth_token, owner_a)

    resp = client.put(
        f"/api/v1/properties/{property_id}/ownership",
        json={
            "ownerships": [
                {"owner_id": owner_a, "ownership_percentage": "30.00"},
                {"owner_id": owner_b, "ownership_percentage": "30.00"},
            ]
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200
