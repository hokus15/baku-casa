"""Contract tests: GET /api/v1/properties and related query endpoints.

Validates response shape, pagination, status codes and error schema against
properties-api-v1.yaml contract (ADR-0006).
Tests execute in RED state until implementation is complete (TDD).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Ana",
    "last_name": "Martínez",
    "legal_name": "Ana Martínez",
    "tax_id": "87654321X",
    "fiscal_address_line1": "Calle Serrano 10",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}

_PROPERTY_PAYLOAD = {
    "name": "Apartamento 3B",
    "type": "APARTAMENTO",
    "ownerships": [
        {"owner_id": "__OWNER_ID__", "ownership_percentage": "100.00"},
    ],
}


def _create_owner(
    client: TestClient, auth_token: str, tax_id: str | None = None
) -> str:
    payload = {**_OWNER_PAYLOAD}
    if tax_id:
        payload["tax_id"] = tax_id
    resp = client.post(
        "/api/v1/owners",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def _create_property(
    client: TestClient, auth_token: str, owner_id: str, name: str = "Prop"
) -> str:
    payload = {
        **_PROPERTY_PAYLOAD,
        "name": name,
        "ownerships": [
            {"owner_id": owner_id, "ownership_percentage": "100.00"}
        ],
    }
    resp = client.post(
        "/api/v1/properties",
        json=payload,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["property_id"]


# ---------------------------------------------------------------------------
# GET /api/v1/properties
# ---------------------------------------------------------------------------


def test_list_properties_returns_200(
    auth_token: str, client: TestClient
) -> None:
    resp = client.get(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_list_properties_response_has_pagination_fields(
    auth_token: str, client: TestClient
) -> None:
    resp = client.get(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert "items" in body
    assert "total" in body
    assert "page" in body
    assert "page_size" in body


def test_list_properties_returns_created_property(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, tax_id="99991111Q")
    property_id = _create_property(
        client, auth_token, owner_id, name="QueryContractProp"
    )
    resp = client.get(
        "/api/v1/properties",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    ids = [p["property_id"] for p in resp.json()["items"]]
    assert property_id in ids


def test_list_properties_returns_401_without_auth(client: TestClient) -> None:
    resp = client.get("/api/v1/properties")
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# GET /api/v1/properties/{property_id}
# ---------------------------------------------------------------------------


def test_get_property_returns_200(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token, tax_id="99992222R")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.get(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_get_property_response_shape(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, tax_id="99993333S")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.get(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert body["property_id"] == property_id
    assert "name" in body
    assert "type" in body
    assert "ownerships" in body
    assert isinstance(body["ownerships"], list)


def test_get_property_returns_404_for_unknown_id(
    auth_token: str, client: TestClient
) -> None:
    resp = client.get(
        "/api/v1/properties/non-existent-id",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_get_property_404_error_has_correlation_id(
    auth_token: str, client: TestClient
) -> None:
    resp = client.get(
        "/api/v1/properties/does-not-exist",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert "error_code" in body
    assert "correlation_id" in body


def test_get_property_returns_401_without_auth(client: TestClient) -> None:
    resp = client.get("/api/v1/properties/any-id")
    assert resp.status_code == 401


# ---------------------------------------------------------------------------
# GET /api/v1/properties/{property_id}/owners
# ---------------------------------------------------------------------------


def test_list_property_owners_returns_200(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, tax_id="99994444T")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.get(
        f"/api/v1/properties/{property_id}/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_list_property_owners_response_has_items(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, tax_id="99995555U")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.get(
        f"/api/v1/properties/{property_id}/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert "items" in body
    assert len(body["items"]) == 1


def test_list_property_owners_returns_404_for_unknown_property(
    auth_token: str, client: TestClient
) -> None:
    resp = client.get(
        "/api/v1/properties/does-not-exist/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /api/v1/owners/{owner_id}/properties
# ---------------------------------------------------------------------------


def test_list_owner_properties_returns_200(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, tax_id="99996666V")
    _create_property(client, auth_token, owner_id)
    resp = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_list_owner_properties_returns_created_property(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, tax_id="99997777W")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    ids = [p["property_id"] for p in body["items"]]
    assert property_id in ids


def test_list_owner_properties_returns_401_without_auth(
    client: TestClient,
) -> None:
    resp = client.get("/api/v1/owners/some-id/properties")
    assert resp.status_code == 401
