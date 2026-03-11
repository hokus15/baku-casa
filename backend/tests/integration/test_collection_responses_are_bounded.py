"""Integration tests: collection responses are always bounded (FR-001, FR-002).

Validates that list/search endpoints for F-0002 and F-0003 never return
unbounded result sets — even when many records exist and no explicit
page_size is provided by the caller.

These tests exercise the actual storage layer through the full HTTP stack
(TestClient + SQLite in-memory).
"""

from __future__ import annotations

from fastapi.testclient import TestClient

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Integracion",
    "last_name": "Acotada",
    "legal_name": "Integracion Acotada SL",
    "fiscal_address_line1": "Calle Test 1",
    "fiscal_address_city": "Barcelona",
    "fiscal_address_postal_code": "08001",
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


def _create_property(
    client: TestClient, token: str, owner_id: str, name: str
) -> str:
    resp = client.post(
        "/api/v1/properties",
        json={
            "name": name,
            "type": "APARTAMENTO",
            "ownerships": [
                {"owner_id": owner_id, "ownership_percentage": "100.00"}
            ],
        },
        headers=_auth_header(token),
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["property_id"]


# ---------------------------------------------------------------------------
# F-0002: owners list is bounded
# ---------------------------------------------------------------------------


def test_owners_list_is_bounded_page_size_never_exceeds_max(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """Response page_size must never exceed PAGINATION_MAX_PAGE_SIZE even when
    caller requests a higher value."""
    from baku.backend.infrastructure.config.pagination_settings import (
        reset_pagination_settings,
    )

    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "5")
    reset_pagination_settings()

    # Create 6 owners — more than the configured max
    for i in range(6):
        _create_owner(client, auth_token, f"C8800{i:04d}")

    resp = client.get(
        "/api/v1/owners",
        params={"page_size": 100},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert (
        len(body["items"]) <= 5
    ), f"Expected at most 5 items (max_page_size=5), got {len(body['items'])}"
    assert body["page_size"] <= 5


def test_owners_list_respects_explicit_page_size_below_max(
    auth_token: str, client: TestClient
) -> None:
    """page_size parameter is respected when below maximum."""
    for i in range(5):
        _create_owner(client, auth_token, f"D8800{i:04d}")

    body = client.get(
        "/api/v1/owners",
        params={"page_size": 2},
        headers=_auth_header(auth_token),
    ).json()
    assert body["page_size"] == 2
    assert len(body["items"]) == 2
    assert body["total"] == 5


def test_owners_list_pagination_total_is_accurate(
    auth_token: str, client: TestClient
) -> None:
    """total reflects the full count, not just the current page."""
    for i in range(4):
        _create_owner(client, auth_token, f"E8800{i:04d}")

    body = client.get(
        "/api/v1/owners",
        params={"page_size": 2},
        headers=_auth_header(auth_token),
    ).json()
    assert body["total"] == 4
    assert len(body["items"]) == 2


# ---------------------------------------------------------------------------
# F-0003: properties list is bounded
# ---------------------------------------------------------------------------


def test_properties_list_is_bounded_page_size_never_exceeds_max(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """Response page_size must never exceed PAGINATION_MAX_PAGE_SIZE."""
    from baku.backend.infrastructure.config.pagination_settings import (
        reset_pagination_settings,
    )

    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "3")
    reset_pagination_settings()

    owner_id = _create_owner(client, auth_token, "F0010001")
    for i in range(5):
        _create_property(client, auth_token, owner_id, f"Propiedad {i}")

    resp = client.get(
        "/api/v1/properties",
        params={"page_size": 100},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert (
        len(body["items"]) <= 3
    ), f"Expected at most 3 items (max_page_size=3), got {len(body['items'])}"


def test_properties_list_respects_explicit_page_size_below_max(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "F0020001")
    for i in range(4):
        _create_property(client, auth_token, owner_id, f"Prop {i}")

    body = client.get(
        "/api/v1/properties",
        params={"page_size": 2},
        headers=_auth_header(auth_token),
    ).json()
    assert body["page_size"] == 2
    assert len(body["items"]) == 2
    assert body["total"] == 4


# ---------------------------------------------------------------------------
# F-0003: owner properties cross-query is bounded
# ---------------------------------------------------------------------------


def test_owner_properties_list_is_bounded(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """Cross-query /owners/{id}/properties must also respect max_page_size."""
    from baku.backend.infrastructure.config.pagination_settings import (
        reset_pagination_settings,
    )

    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "2")
    reset_pagination_settings()

    owner_id = _create_owner(client, auth_token, "G0010001")
    for i in range(4):
        _create_property(client, auth_token, owner_id, f"OwnerProp {i}")

    resp = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        params={"page_size": 100},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["items"]) <= 2
