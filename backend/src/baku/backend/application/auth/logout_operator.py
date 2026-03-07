"""Use case: Logout operator — persist RevokedToken for current jti.

Creates a RevokedToken with reason=logout so the jti cannot be reused.
"""

from __future__ import annotations

import logging

from baku.backend.application.auth.token_validator import TokenClaims
from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.entities import RevocationReason, RevokedToken
from baku.backend.domain.auth.repositories import RevokedTokenRepository, UnitOfWorkPort

logger = logging.getLogger(__name__)


def logout_operator(
    claims: TokenClaims,
    revoked_repo: RevokedTokenRepository,
    uow: UnitOfWorkPort,
) -> None:
    """Revoke the current token explicitly. Idempotent if jti already revoked."""
    logger.info(
        "logout_operator_started",
        extra={"operation": "logout_operator", "operator_id": claims.sub},
    )
    if revoked_repo.is_revoked(claims.jti):
        logger.info(
            "logout_operator_already_revoked",
            extra={"operation": "logout_operator", "operator_id": claims.sub},
        )
        return  # already revoked — idempotent

    revoked = RevokedToken(
        token_jti=claims.jti,
        operator_id=claims.sub,
        revoked_at=utcnow(),
        expires_at=claims.exp,
        reason=RevocationReason.LOGOUT,
    )
    revoked_repo.save(revoked)
    uow.commit()
    logger.info(
        "logout_operator_completed",
        extra={"operation": "logout_operator", "operator_id": claims.sub},
    )
