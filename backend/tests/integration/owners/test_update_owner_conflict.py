"""Integration tests: Update owner — tax_id conflict and immutable id — US4."""

from __future__ import annotations

from fastapi.testclient import TestClient

_BASE = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Owner",
    "last_name": "Update",
    "fiscal_address_line1": "Calle Update 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}


def _create(client: TestClient, token: str, legal_name: str, tax_id: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json={**_BASE, "legal_name": legal_name, "tax_id": tax_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def test_update_tax_id_conflict_with_other_active_owner(auth_token: str, client: TestClient) -> None:
    owner_a = _create(client, auth_token, "Owner A", "CONFLICT001")
    _create(client, auth_token, "Owner B", "CONFLICT002")
    resp = client.patch(
        f"/api/v1/owners/{owner_a}",
        json={"tax_id": "CONFLICT002"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 409
    assert resp.json()["error_code"] == "OWNER_TAX_ID_CONFLICT"


def test_update_same_tax_id_is_allowed(auth_token: str, client: TestClient) -> None:
    """Updating an owner with its own tax_id must not raise conflict."""
    owner_id = _create(client, auth_token, "Same TaxId Owner", "SAMEDTAXID")
    resp = client.patch(
        f"/api/v1/owners/{owner_id}",
        json={"tax_id": "SAMEDTAXID"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200
