"""Contract tests: DELETE /api/v1/properties/{id}.

Validates response shape, status codes and cascade behaviour contract against
properties-api-v1.yaml (ADR-0006).
Tests execute in RED state until implementation is complete (TDD).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Rosa",
    "last_name": "Alonso",
    "legal_name": "Rosa Alonso Vega",
    "tax_id": "55556666E",
    "fiscal_address_line1": "Calle Alcalá 50",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28014",
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
    client: TestClient,
    auth_token: str,
    owner_id: str,
    name: str = "Prop Delete",
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
# DELETE /api/v1/properties/{property_id}
# ---------------------------------------------------------------------------


def test_delete_property_returns_204(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "11119999J")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 204


def test_delete_property_response_body_is_empty(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "22228888K")
    property_id = _create_property(client, auth_token, owner_id)
    resp = client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.content == b""


def test_delete_property_makes_property_not_found_on_get(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "33337777L")
    property_id = _create_property(client, auth_token, owner_id)
    client.delete(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    resp = client.get(
        f"/api/v1/properties/{property_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    # Default get excludes deleted items
    assert resp.status_code == 404


def test_delete_property_returns_404_for_unknown_id(
    auth_token: str, client: TestClient
) -> None:
    resp = client.delete(
        "/api/v1/properties/does-not-exist",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 404


def test_delete_property_returns_401_without_auth(client: TestClient) -> None:
    resp = client.delete("/api/v1/properties/some-id")
    assert resp.status_code == 401


def test_delete_property_404_error_has_correlation_id(
    auth_token: str, client: TestClient
) -> None:
    resp = client.delete(
        "/api/v1/properties/does-not-exist",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = resp.json()
    assert "error_code" in body
    assert "correlation_id" in body
