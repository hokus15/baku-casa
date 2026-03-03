"""Use case: Change operator password — increments credential_version atomically.

Incrementing credential_version invalidates ALL tokens issued under the prior
version (ADR-0005). updated_at is set only on effective modification (FR-021).
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.errors import InvalidCredentials
from baku.backend.infrastructure.persistence.sqlite.auth_repositories import (
    SqliteOperatorRepository,
)
from baku.backend.infrastructure.security.password_hasher import (
    hash_password,
    verify_password,
)


def change_operator_password(
    operator_id: str,
    current_password: str,
    new_password: str,
    session: Session,
) -> None:
    """Rotate password. Raises InvalidCredentials if current_password is wrong."""
    repo = SqliteOperatorRepository(session)
    operator = repo.find_active()

    if operator is None or operator.operator_id != operator_id:
        raise InvalidCredentials()

    if not verify_password(current_password, operator.password_hash):
        raise InvalidCredentials()

    now = utcnow()
    operator.rotate_password(hash_password(new_password), now)
    repo.save(operator)
    session.commit()
