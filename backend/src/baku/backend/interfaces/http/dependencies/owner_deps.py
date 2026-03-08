"""Abstract dependency stubs for owners — per-request repository instances (ADR-0002).

Concrete implementations are provided via app.dependency_overrides in
the composition root (dependency_wiring.py).
"""

from __future__ import annotations

from fastapi import Depends

from baku.backend.domain.owners.repositories import OwnerRepository, OwnerUnitOfWorkPort
from baku.backend.interfaces.http.dependencies.db_session import get_session  # noqa: F401


def get_owner_repo(
    _session: object = Depends(get_session),
) -> OwnerRepository:
    raise NotImplementedError(
        "get_owner_repo not wired — add app.dependency_overrides[get_owner_repo] in dependency_wiring.py"
    )


def get_owner_unit_of_work(
    _session: object = Depends(get_session),
) -> OwnerUnitOfWorkPort:
    raise NotImplementedError(
        "get_owner_unit_of_work not wired "
        "— add app.dependency_overrides[get_owner_unit_of_work] in dependency_wiring.py"
    )
