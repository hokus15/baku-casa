"""Integration tests: create property with initial ownership — F-0003 US1.

Tests verify end-to-end flows including audit metadata, domain invariants,
and state stored in the database.
"""

from __future__ import annotations

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient


def _create_owner(client: TestClient, auth_token: str, tax_id: str = "12345678Z") -> str:
    resp = client.post(
        "/api/v1/owners",
        json={
            "entity_type": "PERSONA_FISICA",
            "first_name": "Maria",
            "last_name": "Lopez",
            "legal_name": "Maria Lopez",
            "tax_id": tax_id,
            "fiscal_address_line1": "Calle Sol 1",
            "fiscal_address_city": "Madrid",
            "fiscal_address_postal_code": "28001",
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def test_create_property_stores_audit_metadata(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Piso en Madrid",
            "type": "VIVIENDA",
            "ownerships": [{"owner_id": owner_id, "ownership_percentage": "100.00"}],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert "created_at" in body
    assert "updated_at" in body
    assert "created_by" in body
    assert body["created_by"] is not None


def test_create_property_with_partial_ownership_accepted(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Piso parcial",
            "type": "VIVIENDA",
            "ownerships": [{"owner_id": owner_id, "ownership_percentage": "50.00"}],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["ownerships"][0]["ownership_percentage"] == "50.00"


def test_create_property_with_multiple_owners_accepted(auth_token: str, client: TestClient) -> None:
    owner_id1 = _create_owner(client, auth_token, tax_id="12345678Z")
    owner_id2 = _create_owner(client, auth_token, tax_id="87654321Z")
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Piso compartido",
            "type": "VIVIENDA",
            "ownerships": [
                {"owner_id": owner_id1, "ownership_percentage": "60.00"},
                {"owner_id": owner_id2, "ownership_percentage": "40.00"},
            ],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert len(body["ownerships"]) == 2


def test_create_property_with_optional_fields(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Local comercial",
            "type": "LOCAL_COMERCIAL",
            "address": "Calle Comercio 5",
            "city": "Barcelona",
            "postal_code": "08001",
            "province": "Barcelona",
            "country": "ES",
            "cadastral_reference": "1234567AB1234C0001XY",
            "cadastral_value": "150000.00",
            "cadastral_land_value": "50000.00",
            "acquisition_date": "2020-01-15",
            "acquisition_type": "ONEROSA",
            "fiscal_nature": "URBANA",
            "fiscal_situation": "CON_REFERENCIA_CATASTRAL",
            "ownerships": [{"owner_id": owner_id, "ownership_percentage": "100.00"}],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["address"] == "Calle Comercio 5"
    assert body["city"] == "Barcelona"
    assert "cadastral_construction_value" in body
    assert "construction_ratio" in body


def test_create_property_derived_cadastral_fields_computed(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Piso con catastro",
            "type": "VIVIENDA",
            "cadastral_value": "200000.00",
            "cadastral_land_value": "60000.00",
            "ownerships": [{"owner_id": owner_id, "ownership_percentage": "100.00"}],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["cadastral_construction_value"] == "140000.00"
    assert "construction_ratio" in body


def test_create_property_rejects_duplicate_owner_in_same_request(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Duplicado",
            "type": "VIVIENDA",
            "ownerships": [
                {"owner_id": owner_id, "ownership_percentage": "50.00"},
                {"owner_id": owner_id, "ownership_percentage": "50.00"},
            ],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 409
    assert resp.json()["error_code"] == "OWNERSHIP_DUPLICATE_ACTIVE_PAIR"


def test_create_property_rejects_land_value_exceeding_total(auth_token: str, client: TestClient) -> None:
    owner_id = _create_owner(client, auth_token)
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": "Incoherente",
            "type": "VIVIENDA",
            "cadastral_value": "100000.00",
            "cadastral_land_value": "150000.00",
            "ownerships": [{"owner_id": owner_id, "ownership_percentage": "100.00"}],
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 400
