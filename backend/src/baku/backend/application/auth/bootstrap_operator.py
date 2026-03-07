"""Use case: Bootstrap initial operator credentials.

Precondition: no Operator exists.
Post: Operator created with credential_version=1, is_active=True.
Raises BootstrapAlreadyCompleted if an operator already exists
(FR-001, FR-002).
"""

from __future__ import annotations

import logging

from baku.backend.application.auth.password_hasher_port import PasswordHasherPort
from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.entities import Operator
from baku.backend.domain.auth.errors import BootstrapAlreadyCompleted
from baku.backend.domain.auth.repositories import OperatorRepository, UnitOfWorkPort

logger = logging.getLogger(__name__)


def bootstrap_operator(
    username: str,
    password: str,
    op_repo: OperatorRepository,
    hasher: PasswordHasherPort,
    uow: UnitOfWorkPort,
) -> Operator:
    """Bootstrap the single operator. Raises BootstrapAlreadyCompleted if already done."""
    logger.info("bootstrap_operator_started", extra={"operation": "bootstrap_operator", "username": username})
    if op_repo.find_active() is not None:
        logger.warning("bootstrap_operator_conflict", extra={"operation": "bootstrap_operator"})
        raise BootstrapAlreadyCompleted()

    operator = Operator.new(
        username=username,
        password_hash=hasher.hash(password),
        now=utcnow(),
    )
    op_repo.save(operator)
    uow.commit()
    logger.info(
        "bootstrap_operator_completed",
        extra={"operation": "bootstrap_operator", "operator_id": operator.operator_id},
    )
    return operator
