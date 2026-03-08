"""Integration test: dependency override equivalence (US2).

Verifies that wire_dependencies() produces the same dependency override mapping
that was previously inlined in main.py — no override dropped, no new one added.

Spec: FR-003, FR-004 — composition root preserves all existing dependency stubs.
"""

from __future__ import annotations

from fastapi import FastAPI

from baku.backend.interfaces.http.bootstrap.dependency_wiring import wire_dependencies
from baku.backend.interfaces.http.dependencies.db_session import get_session
from baku.backend.interfaces.http.dependencies.owner_deps import (
    get_owner_repo,
    get_owner_unit_of_work,
)
from baku.backend.interfaces.http.dependencies.repo_deps import (
    get_operator_repo,
    get_revoked_token_repo,
    get_throttle_repo,
    get_unit_of_work,
)
from baku.backend.interfaces.http.dependencies.require_auth import get_token_validator
from baku.backend.interfaces.http.dependencies.service_deps import (
    get_auth_policy,
    get_password_hasher,
    get_token_issuer,
)

EXPECTED_OVERRIDES = frozenset(
    {
        get_session,
        get_operator_repo,
        get_revoked_token_repo,
        get_throttle_repo,
        get_unit_of_work,
        get_password_hasher,
        get_token_issuer,
        get_auth_policy,
        get_token_validator,
        get_owner_repo,
        get_owner_unit_of_work,
    }
)


def test_all_expected_dependency_stubs_are_overridden() -> None:
    """wire_dependencies must override every abstract stub previously in main.py."""
    app = FastAPI()
    wire_dependencies(app)
    actual = frozenset(app.dependency_overrides.keys())
    missing = EXPECTED_OVERRIDES - actual
    assert not missing, f"Dependency stubs not overridden: {missing}"


def test_no_unexpected_dependency_overrides_added() -> None:
    """wire_dependencies must not introduce overrides beyond the established set."""
    app = FastAPI()
    wire_dependencies(app)
    actual = frozenset(app.dependency_overrides.keys())
    extra = actual - EXPECTED_OVERRIDES
    assert not extra, f"Unexpected dependency overrides introduced: {extra}"


def test_wire_dependencies_is_idempotent() -> None:
    """Calling wire_dependencies twice must produce the same override set."""
    app = FastAPI()
    wire_dependencies(app)
    first_keys = set(app.dependency_overrides.keys())
    wire_dependencies(app)
    second_keys = set(app.dependency_overrides.keys())
    assert first_keys == second_keys, "wire_dependencies must be idempotent"
