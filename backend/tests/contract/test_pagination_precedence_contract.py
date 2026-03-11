"""Contract tests: pagination configuration precedence for collection surfaces.

Validates that the resolution order `environment variables > config file > defaults`
is respected for pagination parameters when collection endpoints are called
(FR-003, FR-004, SC-003 from 001-pagination-rules-sync spec).

These tests treat the HTTP surface as the contract boundary — they do not
inspect internals, only observable response behavior.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from baku.backend.infrastructure.config.pagination_settings import (
    reset_pagination_settings,
)

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Precedencia",
    "last_name": "Config",
    "legal_name": "Precedencia Config SL",
    "fiscal_address_line1": "Avenida Test 1",
    "fiscal_address_city": "Valencia",
    "fiscal_address_postal_code": "46001",
}


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _create_owner(client: TestClient, token: str, tax_id: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json={**_OWNER_PAYLOAD, "tax_id": tax_id},
        headers=_auth_header(token),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["owner_id"]


# ---------------------------------------------------------------------------
# Precedence: env > defaults
# ---------------------------------------------------------------------------


def test_owners_max_page_size_env_overrides_default(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """env var PAGINATION_MAX_PAGE_SIZE caps page_size even when default is higher."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "3")
    reset_pagination_settings()

    for i in range(5):
        _create_owner(client, auth_token, f"P0010{i:04d}")

    resp = client.get(
        "/api/v1/owners",
        params={"page_size": 100},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert (
        body["page_size"] <= 3
    ), f"env PAGINATION_MAX_PAGE_SIZE=3 must override default (got page_size={body['page_size']})"
    assert len(body["items"]) <= 3


def test_properties_max_page_size_env_overrides_default(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """env var PAGINATION_MAX_PAGE_SIZE caps properties list."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "2")
    reset_pagination_settings()

    owner_id = _create_owner(client, auth_token, "P0020001")
    for i in range(4):
        resp_create = client.post(
            "/api/v1/properties",
            json={
                "name": f"PropP {i}",
                "type": "VIVIENDA",
                "ownerships": [
                    {"owner_id": owner_id, "ownership_percentage": "100.00"}
                ],
            },
            headers=_auth_header(auth_token),
        )
        assert resp_create.status_code == 201, resp_create.text

    resp = client.get(
        "/api/v1/properties",
        params={"page_size": 100},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert (
        body["page_size"] <= 2
    ), f"env PAGINATION_MAX_PAGE_SIZE=2 must override default (got page_size={body['page_size']})"


def test_owner_properties_max_page_size_env_overrides_default(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """env var PAGINATION_MAX_PAGE_SIZE caps cross-query /owners/{id}/properties."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "2")
    reset_pagination_settings()

    owner_id = _create_owner(client, auth_token, "P0030001")
    for i in range(4):
        resp_create = client.post(
            "/api/v1/properties",
            json={
                "name": f"OP {i}",
                "type": "ESTUDIO",
                "ownerships": [
                    {"owner_id": owner_id, "ownership_percentage": "100.00"}
                ],
            },
            headers=_auth_header(auth_token),
        )
        assert resp_create.status_code == 201, resp_create.text

    resp = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        params={"page_size": 100},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["page_size"] <= 2


# ---------------------------------------------------------------------------
# Precedence: response reflects configured values
# ---------------------------------------------------------------------------


def test_pagination_contract_response_page_size_bounded_by_env(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """response.page_size must not exceed the env-configured maximum."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "5")
    reset_pagination_settings()

    resp = client.get(
        "/api/v1/owners",
        params={"page_size": 1000},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["page_size"] <= 5
