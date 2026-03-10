"""Integration tests: soft-delete cascade — F-0003 US4.

Tests verify that deleting a property cascades the soft-delete to all active
ownerships, and that the deleted property is excluded from default queries.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_owner(client: TestClient, auth_token: str, tax_id: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json={
            "entity_type": "PERSONA_FISICA",
            "first_name": "Carlos",
            "last_name": "Mora",
            "legal_name": "Carlos Mora",
            "tax_id": tax_id,
            "fiscal_address_line1": "Ramblas 50",
            "fiscal_address_city": "Barcelona",
            "fiscal_address_postal_code": "08002",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def _create_property(
    client: TestClient,
    auth_token: str,
    owner_id: str,
    extra_owners: list[dict] | None = None,
    name: str = "Piso Cascade",
) -> str:
    ownerships = [{"owner_id": owner_id, "ownership_percentage": "100.00"}]
    if extra_owners:
        ownerships = extra_owners
    resp = client.post(
        "/api/v1/properties",
        json={"name": name, "type": "VIVIENDA", "ownerships": ownerships},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["property_id"]


def test_delete_cascades_to_single_ownership(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "D1111111A")
    property_id = _create_property(client, auth_token, owner_id)

    client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    # Ownerships endpoint should return 404 because property is deleted
    resp = client.get(
        f"/api/v1/properties/{property_id}/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_delete_cascades_to_multiple_ownerships(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "D2222222B")
    owner_b = _create_owner(client, auth_token, "D3333333C")
    property_id = _create_property(
        client,
        auth_token,
        owner_a,
        extra_owners=[
            {"owner_id": owner_a, "ownership_percentage": "60.00"},
            {"owner_id": owner_b, "ownership_percentage": "40.00"},
        ],
    )

    client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    resp = client.get(
        f"/api/v1/properties/{property_id}/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_delete_removes_property_from_owner_properties_list(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "D4444444D")
    property_id = _create_property(
        client, auth_token, owner_id, name="Piso Owner List"
    )

    client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    resp = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    ids = [p["property_id"] for p in resp.json()["items"]]
    assert property_id not in ids


def test_deleting_same_property_twice_returns_404(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "D5555555E")
    property_id = _create_property(
        client, auth_token, owner_id, name="Piso Double Delete"
    )

    client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_delete_stores_deleted_by_on_property(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "D6666666F")
    property_id = _create_property(
        client, auth_token, owner_id, name="Piso Deleted By"
    )

    client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    resp = client.get(
        f"/api/v1/properties/{property_id}?include_deleted=true",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body.get("deleted_at") is not None
    assert body.get("deleted_by") is not None
