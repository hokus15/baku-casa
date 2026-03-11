"""Integration tests: EN-0202 precedence resolution for pagination parameters.

Validates how environment-based pagination settings interact with built-in
defaults when collection endpoints execute real storage queries via SQLite
in-memory (FR-003, FR-004, SC-002 from 001-pagination-rules-sync spec).

These tests complement the existing EN-0202 configuration precedence tests
(backend/tests/integration/configuration/test_precedence_resolution.py) by
exercising an HTTP -> application -> storage round-trip for env-vs-defaults
behaviour rather than inspecting the configuration subsystem in isolation.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from baku.backend.infrastructure.config.runtime_settings import (
    reset_runtime_settings,
)

_OWNER_PAYLOAD = {
    "entity_type": "PERSONA_JURIDICA",
    "first_name": "Intg",
    "last_name": "Precedencia",
    "legal_name": "Intg Precedencia SL",
    "fiscal_address_line1": "Calle Integration 1",
    "fiscal_address_city": "Bilbao",
    "fiscal_address_postal_code": "48001",
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
# env > defaults — pagination.max_page_size
# ---------------------------------------------------------------------------


def test_env_pagination_max_page_size_overrides_builtin_default_for_owners(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """PAGINATION_MAX_PAGE_SIZE env var overrides the built-in default (100).

    Creates more records than the env-configured max, requests the full
    set, and asserts the response is capped at the env value.
    """
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "4")
    reset_runtime_settings()

    for i in range(6):
        _create_owner(client, auth_token, f"IP1{i:05d}")

    resp = client.get(
        "/api/v1/owners",
        params={"page_size": 50},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 6
    assert (
        len(body["items"]) == 4
    ), f"expected 4 items (env max=4), got {len(body['items'])}"
    assert body["page_size"] == 4


def test_env_pagination_max_page_size_overrides_builtin_default_for_properties(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """PAGINATION_MAX_PAGE_SIZE env var overrides the built-in default for properties."""
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "2")
    reset_runtime_settings()

    owner_id = _create_owner(client, auth_token, "IP20001")
    for i in range(5):
        resp_create = client.post(
            "/api/v1/properties",
            json={
                "name": f"IProp {i}",
                "type": "LOCAL_COMERCIAL",
                "ownerships": [
                    {"owner_id": owner_id, "ownership_percentage": "100.00"}
                ],
            },
            headers=_auth_header(auth_token),
        )
        assert resp_create.status_code == 201, resp_create.text

    resp = client.get(
        "/api/v1/properties",
        params={"page_size": 50},
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2
    assert body["page_size"] == 2


# ---------------------------------------------------------------------------
# env > defaults — pagination.default_page_size
# ---------------------------------------------------------------------------


def test_env_pagination_default_page_size_used_when_caller_omits_page_size_owners(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """When PAGINATION_DEFAULT_PAGE_SIZE is set and caller omits page_size,
    response page_size must equal the configured default, not the built-in 20.
    """
    monkeypatch.setenv("PAGINATION_DEFAULT_PAGE_SIZE", "3")
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "50")
    reset_runtime_settings()

    for i in range(5):
        _create_owner(client, auth_token, f"IP3{i:05d}")

    resp = client.get(
        "/api/v1/owners",
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    # The endpoint must apply the env-configured default (3), not the hardcoded 20
    assert body["page_size"] == 3, (
        f"env PAGINATION_DEFAULT_PAGE_SIZE=3 must be used as default "
        f"(got page_size={body['page_size']})"
    )
    assert len(body["items"]) == 3


def test_env_pagination_default_page_size_used_when_caller_omits_page_size_properties(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """PAGINATION_DEFAULT_PAGE_SIZE is used as default page_size for properties list."""
    monkeypatch.setenv("PAGINATION_DEFAULT_PAGE_SIZE", "2")
    monkeypatch.setenv("PAGINATION_MAX_PAGE_SIZE", "50")
    reset_runtime_settings()

    owner_id = _create_owner(client, auth_token, "IP40001")
    for i in range(4):
        resp_create = client.post(
            "/api/v1/properties",
            json={
                "name": f"IPropD {i}",
                "type": "APARTAMENTO",
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
    assert resp.status_code == 200
    body = resp.json()
    assert body["page_size"] == 2, (
        f"env PAGINATION_DEFAULT_PAGE_SIZE=2 must be used as default "
        f"(got page_size={body['page_size']})"
    )
    assert len(body["items"]) == 2


# ---------------------------------------------------------------------------
# built-in default when env absent
# ---------------------------------------------------------------------------


def test_builtin_default_page_size_is_20_when_env_absent(
    auth_token: str, client: TestClient, monkeypatch
) -> None:
    """When no env override is set, registered default (20) applies."""
    monkeypatch.delenv("PAGINATION_DEFAULT_PAGE_SIZE", raising=False)
    monkeypatch.delenv("PAGINATION_MAX_PAGE_SIZE", raising=False)
    reset_runtime_settings()

    resp = client.get(
        "/api/v1/owners",
        headers=_auth_header(auth_token),
    )
    assert resp.status_code == 200
    body = resp.json()
    # Built-in default in runtime_settings.py is 20
    assert body["page_size"] == 20
