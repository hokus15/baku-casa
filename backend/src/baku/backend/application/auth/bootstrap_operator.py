"""Use case: Bootstrap initial operator credentials.

Precondition: no Operator exists.
Post: Operator created with credential_version=1, is_active=True.
Raises BootstrapAlreadyCompleted if an operator already exists
(FR-001, FR-002).
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.entities import Operator
from baku.backend.domain.auth.errors import BootstrapAlreadyCompleted
from baku.backend.infrastructure.persistence.sqlite.auth_repositories import (
    SqliteOperatorRepository,
)
from baku.backend.infrastructure.security.password_hasher import hash_password


def bootstrap_operator(username: str, password: str, session: Session) -> Operator:
    """Bootstrap the single operator. Raises BootstrapAlreadyCompleted if already done."""
    repo = SqliteOperatorRepository(session)

    if repo.find_active() is not None:
        raise BootstrapAlreadyCompleted()

    now = utcnow()
    operator = Operator.new(
        username=username,
        password_hash=hash_password(password),
        now=now,
    )
    repo.save(operator)
    session.commit()
    return operator
