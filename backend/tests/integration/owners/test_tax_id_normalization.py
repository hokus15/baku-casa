"""Integration tests: tax_id normalization — US1."""

from __future__ import annotations

from fastapi.testclient import TestClient

_BASE = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Test",
    "last_name": "Normalization",
    "legal_name": "Test Normalization",
    "fiscal_address_line1": "Calle Ejemplo 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}


def test_normalized_tax_id_is_stored(auth_token: str, client: TestClient) -> None:
    payload = {**_BASE, "tax_id": " 12 345 678-z "}
    resp = client.post("/api/v1/owners", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert resp.status_code == 201
    assert resp.json()["tax_id"] == "12345678Z"


def test_duplicate_tax_id_detected_after_normalization(auth_token: str, client: TestClient) -> None:
    """Same logical tax_id in different formats must be detected as duplicate."""
    client.post(
        "/api/v1/owners",
        json={**_BASE, "tax_id": "12345678Z"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    # Format variant: lowercase with hyphen and spaces
    resp = client.post(
        "/api/v1/owners",
        json={**_BASE, "tax_id": " 12-345-678 z ", "legal_name": "Other"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 409


def test_tax_id_filter_uses_normalized_form(auth_token: str, client: TestClient) -> None:
    client.post(
        "/api/v1/owners",
        json={**_BASE, "tax_id": "12345678Z"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    # Search with variant form
    resp = client.get(
        "/api/v1/owners?tax_id=12345678z",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["total"] == 1
