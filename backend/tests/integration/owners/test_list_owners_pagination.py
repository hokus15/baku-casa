"""Integration tests: List owners with pagination — US3."""

from __future__ import annotations

from fastapi.testclient import TestClient

_BASE = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Owner",
    "last_name": "Paginacion",
    "fiscal_address_line1": "Calle Paginacion 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}


def _mk_payload(n: int) -> dict:
    return {**_BASE, "legal_name": f"Owner Paginacion {n}", "tax_id": f"PAGTEST{n:04d}"}


def test_pagination_returns_correct_page(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    for i in range(5):
        client.post("/api/v1/owners", json=_mk_payload(i), headers=headers)

    resp = client.get("/api/v1/owners?page=1&page_size=3", headers=headers)
    body = resp.json()
    assert body["total"] == 5
    assert len(body["items"]) == 3
    assert body["page"] == 1
    assert body["page_size"] == 3


def test_pagination_second_page(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    for i in range(5):
        client.post("/api/v1/owners", json=_mk_payload(i), headers=headers)

    resp = client.get("/api/v1/owners?page=2&page_size=3", headers=headers)
    body = resp.json()
    assert len(body["items"]) == 2
    assert body["page"] == 2


def test_page_size_capped_at_100(auth_token: str, client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {auth_token}"}
    resp = client.get("/api/v1/owners?page_size=999", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["page_size"] <= 100
