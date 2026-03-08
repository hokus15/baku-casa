"""Contract tests: GET /api/v1/owners."""

from __future__ import annotations

from fastapi.testclient import TestClient

_VALID_PAYLOAD = {
    "entity_type": "PERSONA_JURIDICA",
    "first_name": "Empresa",
    "last_name": "SL",
    "legal_name": "Empresa SL",
    "tax_id": "B12345678",
    "fiscal_address_line1": "Gran Vía 10",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28013",
}


def test_list_owners_returns_200(auth_token: str, client: TestClient) -> None:
    resp = client.get(
        "/api/v1/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert resp.status_code == 200


def test_list_owners_response_matches_schema(auth_token: str, client: TestClient) -> None:
    body = client.get(
        "/api/v1/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    ).json()
    assert "items" in body
    assert "total" in body
    assert "page" in body
    assert "page_size" in body


def test_list_owners_empty_list_is_valid(auth_token: str, client: TestClient) -> None:
    body = client.get(
        "/api/v1/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    ).json()
    assert body["items"] == []
    assert body["total"] == 0


def test_list_owners_returns_401_without_auth(client: TestClient) -> None:
    resp = client.get("/api/v1/owners")
    assert resp.status_code == 401


def test_list_owners_returns_created_owner(auth_token: str, client: TestClient) -> None:
    client.post(
        "/api/v1/owners",
        json=_VALID_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    body = client.get(
        "/api/v1/owners",
        headers={"Authorization": f"Bearer {auth_token}"},
    ).json()
    assert body["total"] == 1
    assert len(body["items"]) == 1
