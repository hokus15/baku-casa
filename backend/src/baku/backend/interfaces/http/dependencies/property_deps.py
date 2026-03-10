"""Abstract dependency stubs for properties — per-request repository instances (ADR-0002).

Concrete implementations are provided via app.dependency_overrides in
the composition root (dependency_wiring.py).
"""

from __future__ import annotations

from fastapi import Depends

from baku.backend.domain.properties.repositories import (
    OwnershipRepository,
    PropertyRepository,
    PropertyUnitOfWorkPort,
)
from baku.backend.interfaces.http.dependencies.db_session import (
    get_session,
)  # noqa: F401


def get_property_repo(
    _session: object = Depends(get_session),
) -> PropertyRepository:
    raise NotImplementedError(
        "get_property_repo not wired — add app.dependency_overrides[get_property_repo] in dependency_wiring.py"
    )


def get_ownership_repo(
    _session: object = Depends(get_session),
) -> OwnershipRepository:
    raise NotImplementedError(
        "get_ownership_repo not wired — add app.dependency_overrides[get_ownership_repo] in dependency_wiring.py"
    )


def get_property_unit_of_work(
    _session: object = Depends(get_session),
) -> PropertyUnitOfWorkPort:
    raise NotImplementedError(
        "get_property_unit_of_work not wired "
        "— add app.dependency_overrides[get_property_unit_of_work] in dependency_wiring.py"
    )
