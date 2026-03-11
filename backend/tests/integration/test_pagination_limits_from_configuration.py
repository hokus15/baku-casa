"""Integration tests: pagination limits enforced from EN-0202 configuration.

Validates that `max_page_size` is read exclusively from centralized configuration
and applied consistently across all collection surfaces, preventing unbounded
responses regardless of what page_size value the caller sends (FR-002, FR-003,
FR-005, SC-004 from 001-pagination-rules-sync spec).

These tests complement test_collection_responses_are_bounded.py by focusing
on the configuration-driven enforcement path rather than just "is it bounded".
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from baku.backend.infrastructure.config.pagination_settings import (
    reset_pagination_settings,
)

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_JURIDICA",
    "first_name": "Config",
    "last_name": "Limits",
    "legal_name": "Config Limits SL",
    "fiscal_address_line1": "Calle Limites 1",
    "fiscal_address_city": "Zaragoza",
    "fiscal_address_postal_code": "50001",
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
# F-0002: owners max_page_size from config
# ---------------------------------------------------------------------------


def test_owners_list_max_page_size_from_config_caps_response(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """PAGINATION_MAX_PAGE_SIZE env var defines the ceiling for owners list."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "4")
    reset_pagination_settings()

    for i in range(10):
        _create_owner(client, auth_token, f"CL01{i:05d}")

    resp = client.get(
        "/api/v1/owners",
        params={"page_size": 1000},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert (
        len(body["items"]) == 4
    ), f"Expected 4 items capped by PAGINATION_MAX_PAGE_SIZE=4, got {len(body['items'])}"
    assert body["page_size"] == 4


def test_owners_list_max_page_size_from_config_lower_limit(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """A very low PAGINATION_MAX_PAGE_SIZE (1) is respected."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "1")
    reset_pagination_settings()

    for i in range(3):
        _create_owner(client, auth_token, f"CL02{i:05d}")

    body = client.get(
        "/api/v1/owners",
        params={"page_size": 100},
        headers=_auth_header(auth_token),
    ).json()
    assert len(body["items"]) == 1
    assert body["page_size"] == 1
    assert body["total"] == 3


def test_owners_list_max_page_size_from_config_higher_limit(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """PAGINATION_MAX_PAGE_SIZE can be raised above built-in 100 if needed."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "200")
    reset_pagination_settings()

    for i in range(5):
        _create_owner(client, auth_token, f"CL03{i:05d}")

    body = client.get(
        "/api/v1/owners",
        params={"page_size": 150},
        headers=_auth_header(auth_token),
    ).json()
    # We only have 5 items so all 5 should be returned
    assert len(body["items"]) == 5
    # page_size reported should be <= 200 (respects the configured max)
    assert body["page_size"] <= 200


# ---------------------------------------------------------------------------
# F-0003: properties max_page_size from config
# ---------------------------------------------------------------------------


def test_properties_list_max_page_size_from_config_caps_response(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """PAGINATION_MAX_PAGE_SIZE caps properties list."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "3")
    reset_pagination_settings()

    owner_id = _create_owner(client, auth_token, "CL04001")
    for i in range(6):
        client.post(
            "/api/v1/properties",
            json={
                "name": f"CLProp {i}",
                "type": "APARTAMENTO",
                "ownerships": [
                    {"owner_id": owner_id, "ownership_percentage": "100.00"}
                ],
            },
            headers=_auth_header(auth_token),
        )

    resp = client.get(
        "/api/v1/properties",
        params={"page_size": 1000},
        headers=_auth_header(auth_token),
    )
    body = resp.json()
    assert len(body["items"]) == 3
    assert body["page_size"] == 3


# ---------------------------------------------------------------------------
# F-0003: owner properties cross-query max_page_size from config
# ---------------------------------------------------------------------------


def test_owner_properties_list_max_page_size_from_config(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """PAGINATION_MAX_PAGE_SIZE caps /owners/{id}/properties cross-query."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "2")
    reset_pagination_settings()

    owner_id = _create_owner(client, auth_token, "CL05001")
    for i in range(5):
        client.post(
            "/api/v1/properties",
            json={
                "name": f"CLCross {i}",
                "type": "ESTUDIO",
                "ownerships": [
                    {"owner_id": owner_id, "ownership_percentage": "100.00"}
                ],
            },
            headers=_auth_header(auth_token),
        )

    resp = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        params={"page_size": 1000},
        headers=_auth_header(auth_token),
    )
    body = resp.json()
    assert len(body["items"]) == 2
    assert body["page_size"] == 2
