"""Contract regression tests: no hardcoded pagination defaults outside EN-0202.

Validates that pagination defaults are NOT hardcoded in routers — all
collection endpoints must use the value from centralized configuration
(FR-005, SC-004 from 001-pagination-rules-sync spec).

THE KEY INVARIANT: if PAGINATION_DEFAULT_PAGE_SIZE is set via env var to a
non-default value (e.g. 5), calling a collection endpoint WITHOUT an explicit
page_size query parameter must return page_size == 5, NOT the built-in 20.

A test failure here indicates a hardcoded `default=20` in an HTTP router's
Query parameter that bypasses centralized configuration.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from baku.backend.infrastructure.config.pagination_settings import (
    reset_pagination_settings,
)

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "NoHardcode",
    "last_name": "Test",
    "legal_name": "NoHardcode Test SL",
    "fiscal_address_line1": "Calle Regresion 1",
    "fiscal_address_city": "Sevilla",
    "fiscal_address_postal_code": "41001",
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
# F-0002: owners — no hardcoded default_page_size
# ---------------------------------------------------------------------------


def test_owners_list_default_page_size_comes_from_config_not_hardcode(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """When PAGINATION_DEFAULT_PAGE_SIZE=5, calling GET /owners without page_size
    must return page_size=5, proving the default is read from config (not hardcoded).

    This is the primary regression guard for FR-005.
    """
    monkeypatch.setenv("PAGINATION_DEFAULT_PAGE_SIZE", "5")
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "50")
    reset_pagination_settings()

    for i in range(8):
        _create_owner(client, auth_token, f"NH01{i:05d}")

    resp = client.get(
        "/api/v1/owners",
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["page_size"] == 5, (
        "FAIL: page_size is not 5 — this means the default page_size is hardcoded "
        f"in the owners router instead of reading from PAGINATION_DEFAULT_PAGE_SIZE env var. "
        f"Got page_size={body['page_size']}"
    )
    assert len(body["items"]) == 5


def test_owners_list_default_page_size_uses_configured_value_not_implicit_20(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """Set default to 3 — unambiguously not 20 — to rule out accidental pass."""
    monkeypatch.setenv("PAGINATION_DEFAULT_PAGE_SIZE", "3")
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "50")
    reset_pagination_settings()

    for i in range(5):
        _create_owner(client, auth_token, f"NH02{i:05d}")

    resp = client.get(
        "/api/v1/owners",
        headers=_auth_header(auth_token),
    )
    body = resp.json()
    assert (
        body["page_size"] == 3
    ), f"Expected page_size=3 from config, got {body['page_size']} (hardcoded default?)"


# ---------------------------------------------------------------------------
# F-0003: properties — no hardcoded default_page_size
# ---------------------------------------------------------------------------


def test_properties_list_default_page_size_comes_from_config_not_hardcode(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """When PAGINATION_DEFAULT_PAGE_SIZE=4, GET /properties without page_size
    must return page_size=4."""
    monkeypatch.setenv("PAGINATION_DEFAULT_PAGE_SIZE", "4")
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "50")
    reset_pagination_settings()

    owner_id = _create_owner(client, auth_token, "NH03001")
    for i in range(6):
        resp_create = client.post(
            "/api/v1/properties",
            json={
                "name": f"NHProp {i}",
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
        headers=_auth_header(auth_token),
    )
    body = resp.json()
    assert (
        body["page_size"] == 4
    ), f"Expected page_size=4 from config, got {body['page_size']} (hardcoded default?)"
    assert len(body["items"]) == 4


# ---------------------------------------------------------------------------
# F-0003: owner properties cross-query — no hardcoded default_page_size
# ---------------------------------------------------------------------------


def test_owner_properties_cross_query_default_page_size_comes_from_config(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """GET /owners/{id}/properties without page_size must use configured default."""
    monkeypatch.setenv("PAGINATION_DEFAULT_PAGE_SIZE", "2")
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "50")
    reset_pagination_settings()

    owner_id = _create_owner(client, auth_token, "NH04001")
    for i in range(4):
        resp_create = client.post(
            "/api/v1/properties",
            json={
                "name": f"NHOwnerProp {i}",
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
        headers=_auth_header(auth_token),
    )
    body = resp.json()
    assert (
        body["page_size"] == 2
    ), f"Expected page_size=2 from config, got {body['page_size']} (hardcoded default?)"
    assert len(body["items"]) == 2
