"""Integration tests: List owners with filters — US3."""

from __future__ import annotations

from fastapi.testclient import TestClient

_BASE = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Owner",
    "last_name": "Filtros",
    "fiscal_address_line1": "Calle Filtros 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}


def test_filter_by_tax_id(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post("/api/v1/owners", json={**_BASE, "legal_name": "A", "tax_id": "FILTRO001"}, headers=headers)
    client.post("/api/v1/owners", json={**_BASE, "legal_name": "B", "tax_id": "FILTRO002"}, headers=headers)

    resp = client.get("/api/v1/owners?tax_id=FILTRO001", headers=headers)
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["tax_id"] == "FILTRO001"


def test_filter_by_legal_name_partial(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    client.post(
        "/api/v1/owners", json={**_BASE, "legal_name": "Empresa Alfa SL", "tax_id": "FILNAME001"}, headers=headers
    )  # noqa: E501
    client.post(
        "/api/v1/owners", json={**_BASE, "legal_name": "Empresa Beta SL", "tax_id": "FILNAME002"}, headers=headers
    )  # noqa: E501
    client.post("/api/v1/owners", json={**_BASE, "legal_name": "Other Corp", "tax_id": "FILNAME003"}, headers=headers)

    resp = client.get("/api/v1/owners?legal_name=Empresa", headers=headers)
    body = resp.json()
    assert body["total"] == 2


def test_filter_excludes_deleted_by_default(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.post(
        "/api/v1/owners",
        json={**_BASE, "legal_name": "To Delete", "tax_id": "FILTERDEL1"},
        headers=headers,
    )
    owner_id = resp.json()["owner_id"]
    client.delete(f"/api/v1/owners/{owner_id}", headers=headers)

    resp = client.get("/api/v1/owners", headers=headers)
    assert resp.json()["total"] == 0


def test_filter_include_deleted_shows_deleted(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.post(
        "/api/v1/owners",
        json={**_BASE, "legal_name": "To Delete 2", "tax_id": "FILTERDEL2"},
        headers=headers,
    )
    owner_id = resp.json()["owner_id"]
    client.delete(f"/api/v1/owners/{owner_id}", headers=headers)

    resp = client.get("/api/v1/owners?include_deleted=true", headers=headers)
    assert resp.json()["total"] == 1
