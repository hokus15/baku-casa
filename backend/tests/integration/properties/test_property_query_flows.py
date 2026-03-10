"""Integration tests: query flows — F-0003 US2.

Tests verify end-to-end query flows including pagination, detail retrieval,
cross-queries by owner, and empty states.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def _create_owner(
    client: TestClient, auth_token: str, tax_id: str = "55551111A"
) -> str:
    resp = client.post(
        "/api/v1/owners",
        json={
            "entity_type": "PERSONA_FISICA",
            "first_name": "Pedro",
            "last_name": "Ruiz",
            "legal_name": "Pedro Ruiz",
            "tax_id": tax_id,
            "fiscal_address_line1": "Gran Vía 1",
            "fiscal_address_city": "Madrid",
            "fiscal_address_postal_code": "28013",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def _create_property(
    client: TestClient,
    auth_token: str,
    owner_id: str,
    name: str = "Piso Query",
    pct: str = "100.00",
) -> str:
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": name,
            "type": "VIVIENDA",
            "ownerships": [
                {"owner_id": owner_id, "ownership_percentage": pct}
            ],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["property_id"]


def test_list_properties_pagination_page_and_page_size(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "55552222B")
    _create_property(client, auth_token, owner_id, "Piso Pag 1")
    _create_property(client, auth_token, owner_id, "Piso Pag 2")
    resp = client.get(
        "/api/v1/properties?page=1&page_size=1",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["page"] == 1
    assert body["page_size"] == 1
    assert len(body["items"]) <= 1
    assert body["total"] >= 2


def test_list_properties_second_page(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "55553333C")
    _create_property(client, auth_token, owner_id, "Piso Pag2 A")
    _create_property(client, auth_token, owner_id, "Piso Pag2 B")
    resp = client.get(
        "/api/v1/properties?page=2&page_size=1",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["page"] == 2
    assert len(body["items"]) <= 1


def test_get_property_detail_returns_all_fields(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "55554444D")
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Piso con Detalles",
            "type": "APARTAMENTO",
            "address": "Calle Real 5",
            "city": "Sevilla",
            "postal_code": "41001",
            "ownerships": [
                {"owner_id": owner_id, "ownership_percentage": "100.00"}
            ],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    property_id = resp.json()["property_id"]
    resp2 = client.get(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp2.json()
    assert body["address"] == "Calle Real 5"
    assert body["city"] == "Sevilla"


def test_list_property_owners_returns_correct_percentages(
    auth_token: str, client: TestClient
) -> None:
    owner_a = _create_owner(client, auth_token, "55555555E")
    owner_b = _create_owner(client, auth_token, "55556666F")
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Piso 2 titulares",
            "type": "VIVIENDA",
            "ownerships": [
                {"owner_id": owner_a, "ownership_percentage": "60.00"},
                {"owner_id": owner_b, "ownership_percentage": "40.00"},
            ],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    property_id = resp.json()["property_id"]
    resp2 = client.get(
        f"/api/v1/properties/{property_id}/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp2.json()
    pcts = {o["owner_id"]: o["ownership_percentage"] for o in body["items"]}
    assert "60.00" in pcts[owner_a]
    assert "40.00" in pcts[owner_b]


def test_list_owner_properties_cross_query(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "55557777G")
    p1 = _create_property(client, auth_token, owner_id, "Piso Cross A")
    p2 = _create_property(client, auth_token, owner_id, "Piso Cross B")
    resp = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    ids = [p["property_id"] for p in resp.json()["items"]]
    assert p1 in ids
    assert p2 in ids


def test_deleted_property_not_in_default_list(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "55558888H")
    property_id = _create_property(
        client, auth_token, owner_id, "Piso A Borrar"
    )
    client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = client.get(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    ids = [p["property_id"] for p in resp.json()["items"]]
    assert property_id not in ids


def test_deleted_property_visible_with_include_deleted(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "55559999I")
    property_id = _create_property(
        client, auth_token, owner_id, "Piso Deleted View"
    )
    client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = client.get(
        "/api/v1/properties?include_deleted=true",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    ids = [p["property_id"] for p in resp.json()["items"]]
    assert property_id in ids
