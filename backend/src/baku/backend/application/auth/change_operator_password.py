"""Use case: Change operator password — increments credential_version atomically.

Incrementing credential_version invalidates ALL tokens issued under the prior
version (ADR-0005). updated_at is set only on effective modification (FR-021).
"""

from __future__ import annotations

from baku.backend.application.auth.password_hasher_port import PasswordHasherPort
from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.errors import InvalidCredentials
from baku.backend.domain.auth.repositories import OperatorRepository, UnitOfWorkPort


def change_operator_password(
    operator_id: str,
    current_password: str,
    new_password: str,
    op_repo: OperatorRepository,
    hasher: PasswordHasherPort,
    uow: UnitOfWorkPort,
) -> None:
    """Rotate password. Raises InvalidCredentials if current_password is wrong."""
    operator = op_repo.find_active()

    if operator is None or operator.operator_id != operator_id:
        raise InvalidCredentials()

    if not hasher.verify(current_password, operator.password_hash):
        raise InvalidCredentials()

    operator.rotate_password(hasher.hash(new_password), utcnow())
    op_repo.save(operator)
    uow.commit()
