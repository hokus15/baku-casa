"""Contract tests: mandatory pagination on all collection/list/search surfaces.

Validates that every collection endpoint exposed by F-0002 and F-0003 returns
a bounded, paginated response regardless of how many items exist (ADR-0004,
FR-001 from 001-pagination-rules-sync spec).

Surfaces under test:
  - GET /api/v1/owners               (F-0002 list+search)
  - GET /api/v1/properties           (F-0003 list)
  - GET /api/v1/owners/{id}/properties  (F-0003 cross-query)
"""

from __future__ import annotations

from fastapi.testclient import TestClient

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_FISICA",
    "first_name": "Contrato",
    "last_name": "Paginacion",
    "legal_name": "Contrato Paginacion SL",
    "tax_id": "B99001001",
    "fiscal_address_line1": "Calle Mayor 1",
    "fiscal_address_city": "Madrid",
    "fiscal_address_postal_code": "28001",
}

_PROPERTY_PAYLOAD = {
    "name": "Propiedad Contrato",
    "type": "VIVIENDA",
}


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _create_owner(client: TestClient, token: str, tax_id: str) -> str:
    resp = client.post(
        "/api/v1/owners",
        json={**_OWNER_PAYLOAD, "tax_id": tax_id},
        headers=_auth_header(token),
    )
    assert resp.status_code == 201
    return resp.json()["owner_id"]


def _create_property(client: TestClient, token: str, owner_id: str) -> str:
    resp = client.post(
        "/api/v1/properties",
        json={
            **_PROPERTY_PAYLOAD,
            "ownerships": [
                {"owner_id": owner_id, "ownership_percentage": "100.00"}
            ],
        },
        headers=_auth_header(token),
    )
    assert resp.status_code == 201
    return resp.json()["property_id"]


# ---------------------------------------------------------------------------
# GET /api/v1/owners — F-0002 collection surface
# ---------------------------------------------------------------------------


def test_list_owners_response_has_mandatory_pagination_fields(
    auth_token: str, client: TestClient
) -> None:
    """Response must include page, page_size, total and items (FR-001)."""
    body = client.get(
        "/api/v1/owners",
        headers=_auth_header(auth_token),
    ).json()
    assert "items" in body, "missing 'items' key"
    assert "total" in body, "missing 'total' key"
    assert "page" in body, "missing 'page' key"
    assert "page_size" in body, "missing 'page_size' key"


def test_list_owners_pagination_fields_have_correct_types(
    auth_token: str, client: TestClient
) -> None:
    body = client.get(
        "/api/v1/owners",
        headers=_auth_header(auth_token),
    ).json()
    assert isinstance(body["page"], int)
    assert isinstance(body["page_size"], int)
    assert isinstance(body["total"], int)
    assert isinstance(body["items"], list)


def test_list_owners_page_starts_at_one(
    auth_token: str, client: TestClient
) -> None:
    body = client.get(
        "/api/v1/owners",
        headers=_auth_header(auth_token),
    ).json()
    assert body["page"] == 1


def test_list_owners_returns_bounded_subset_on_explicit_page_size(
    auth_token: str, client: TestClient
) -> None:
    """Requesting page_size=1 must return at most 1 item even with multiple records."""
    for i in range(3):
        _create_owner(client, auth_token, f"B9900{i:04d}")

    body = client.get(
        "/api/v1/owners",
        params={"page_size": 1},
        headers=_auth_header(auth_token),
    ).json()
    assert body["page_size"] == 1
    assert len(body["items"]) <= 1


def test_owners_search_has_mandatory_pagination_fields(
    auth_token: str, client: TestClient
) -> None:
    """Search via filter params must also be paginated (FR-001)."""
    body = client.get(
        "/api/v1/owners",
        params={"legal_name": "no-match"},
        headers=_auth_header(auth_token),
    ).json()
    assert "items" in body
    assert "page" in body
    assert "page_size" in body
    assert "total" in body


# ---------------------------------------------------------------------------
# GET /api/v1/properties — F-0003 collection surface
# ---------------------------------------------------------------------------


def test_list_properties_response_has_mandatory_pagination_fields(
    auth_token: str, client: TestClient
) -> None:
    body = client.get(
        "/api/v1/properties",
        headers=_auth_header(auth_token),
    ).json()
    assert "items" in body
    assert "total" in body
    assert "page" in body
    assert "page_size" in body


def test_list_properties_page_starts_at_one(
    auth_token: str, client: TestClient
) -> None:
    body = client.get(
        "/api/v1/properties",
        headers=_auth_header(auth_token),
    ).json()
    assert body["page"] == 1


def test_list_properties_returns_bounded_subset_on_explicit_page_size(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "B00010001")
    for i in range(3):
        _create_property(client, auth_token, owner_id)

    body = client.get(
        "/api/v1/properties",
        params={"page_size": 1},
        headers=_auth_header(auth_token),
    ).json()
    assert body["page_size"] == 1
    assert len(body["items"]) <= 1


# ---------------------------------------------------------------------------
# GET /api/v1/owners/{owner_id}/properties — F-0003 cross-query surface
# ---------------------------------------------------------------------------


def test_owner_properties_response_has_mandatory_pagination_fields(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "B00020001")

    body = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        headers=_auth_header(auth_token),
    ).json()
    assert "items" in body
    assert "total" in body
    assert "page" in body
    assert "page_size" in body


def test_owner_properties_returns_bounded_subset_on_explicit_page_size(
    auth_token: str, client: TestClient
) -> None:
    owner_id = _create_owner(client, auth_token, "B00030001")
    for i in range(3):
        # Give each property a shared + unique co-owner so tax_ids don't collide
        extra_owner_id = _create_owner(client, auth_token, f"B0004{i:04d}")
        client.post(
            "/api/v1/properties",
            json={
                "name": f"Prop {i}",
                "type": "VIVIENDA",
                "ownerships": [
                    {"owner_id": owner_id, "ownership_percentage": "50.00"},
                    {
                        "owner_id": extra_owner_id,
                        "ownership_percentage": "50.00",
                    },
                ],
            },
            headers=_auth_header(auth_token),
        )

    body = client.get(
        f"/api/v1/owners/{owner_id}/properties",
        params={"page_size": 1},
        headers=_auth_header(auth_token),
    ).json()
    assert body["page_size"] == 1
    assert len(body["items"]) <= 1
