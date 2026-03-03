"""Use case: Bootstrap initial operator credentials.

Precondition: no Operator exists.
Post: Operator created with credential_version=1, is_active=True.
Raises BootstrapAlreadyCompleted if an operator already exists
(FR-001, FR-002).
"""

from __future__ import annotations

from baku.backend.application.auth.password_hasher_port import PasswordHasherPort
from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.entities import Operator
from baku.backend.domain.auth.errors import BootstrapAlreadyCompleted
from baku.backend.domain.auth.repositories import OperatorRepository, UnitOfWorkPort


def bootstrap_operator(
    username: str,
    password: str,
    op_repo: OperatorRepository,
    hasher: PasswordHasherPort,
    uow: UnitOfWorkPort,
) -> Operator:
    """Bootstrap the single operator. Raises BootstrapAlreadyCompleted if already done."""
    if op_repo.find_active() is not None:
        raise BootstrapAlreadyCompleted()

    operator = Operator.new(
        username=username,
        password_hash=hasher.hash(password),
        now=utcnow(),
    )
    op_repo.save(operator)
    uow.commit()
    return operator
