"""Abstract dependency stubs: per-request repository instances (ADR-0002).

Concrete implementations are provided by infrastructure via
app.dependency_overrides in the composition root (main.py).
All stubs raise NotImplementedError so a missing override surfaces
as a clear error rather than a silent wrong result.
"""

from __future__ import annotations

from fastapi import Depends

from baku.backend.domain.auth.repositories import (
    OperatorRepository,
    RevokedTokenRepository,
    ThrottleStateRepository,
    UnitOfWorkPort,
)
from baku.backend.interfaces.http.dependencies.db_session import get_session  # noqa: F401


def get_operator_repo(
    _session: object = Depends(get_session),
) -> OperatorRepository:
    raise NotImplementedError(
        "get_operator_repo not wired — add app.dependency_overrides[get_operator_repo] in main.py"
    )


def get_revoked_token_repo(
    _session: object = Depends(get_session),
) -> RevokedTokenRepository:
    raise NotImplementedError(
        "get_revoked_token_repo not wired — add app.dependency_overrides[get_revoked_token_repo] in main.py"
    )


def get_throttle_repo(
    _session: object = Depends(get_session),
) -> ThrottleStateRepository:
    raise NotImplementedError(
        "get_throttle_repo not wired — add app.dependency_overrides[get_throttle_repo] in main.py"
    )


def get_unit_of_work(
    _session: object = Depends(get_session),
) -> UnitOfWorkPort:
    raise NotImplementedError("get_unit_of_work not wired — add app.dependency_overrides[get_unit_of_work] in main.py")
