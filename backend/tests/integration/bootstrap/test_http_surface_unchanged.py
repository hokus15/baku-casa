"""Integration test: unchanged HTTP surface sentinel (US3).

Verifies that the modularized bootstrap produces the exact same HTTP surface
as the original main.py — no routes added, none removed, no path changes.

Spec: FR-008 — bootstrap evolution must not introduce external contract drift.
ADR-0006 — no contract surface changes in EN-0300.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

# Canonical HTTP surface for the application post-F-0003.
# This set is the immutable sentinel: any deviation is a contract breach.
EXPECTED_ROUTE_METHODS: dict[str, set[str]] = {
    "/api/v1/auth/bootstrap": {"POST"},
    "/api/v1/auth/login": {"POST"},
    "/api/v1/auth/logout": {"POST"},
    "/api/v1/auth/password": {"PUT"},
    "/api/v1/owners": {"POST", "GET"},
    "/api/v1/owners/{owner_id}": {"GET", "PATCH", "DELETE"},
    "/api/v1/owners/{owner_id}/properties": {"GET"},
    "/api/v1/properties": {"POST", "GET"},
    "/api/v1/properties/{property_id}": {"GET", "PATCH", "DELETE"},
    "/api/v1/properties/{property_id}/owners": {"GET"},
    "/api/v1/properties/{property_id}/ownership": {"PUT"},
}


def test_all_expected_routes_are_present(client: TestClient) -> None:
    """All auth routes must be reachable after modularized bootstrap."""
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    paths = set(resp.json()["paths"].keys())
    for route in EXPECTED_ROUTE_METHODS:
        assert (
            route in paths
        ), f"Expected route {route!r} not found in HTTP surface: {paths}"


def test_no_unexpected_routes_added(client: TestClient) -> None:
    """No extra routes should appear after bootstrap modularization (EN-0300 adds no new endpoints)."""
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    paths = set(resp.json()["paths"].keys())
    unexpected = paths - set(EXPECTED_ROUTE_METHODS.keys())
    assert (
        not unexpected
    ), f"Unexpected routes found in HTTP surface: {unexpected}"


def test_route_http_methods_unchanged(client: TestClient) -> None:
    """HTTP methods for each route must match the established surface."""
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    openapi_paths = resp.json()["paths"]
    for path, expected_methods in EXPECTED_ROUTE_METHODS.items():
        actual_methods = {m.upper() for m in openapi_paths[path].keys()}
        assert (
            actual_methods == expected_methods
        ), f"Route {path!r}: expected methods {expected_methods}, got {actual_methods}"
