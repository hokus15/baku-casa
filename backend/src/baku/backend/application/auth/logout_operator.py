"""Use case: Logout operator — persist RevokedToken for current jti.

Creates a RevokedToken with reason=logout so the jti cannot be reused.
"""

from __future__ import annotations

from baku.backend.application.auth.token_validator import TokenClaims
from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.entities import RevocationReason, RevokedToken
from baku.backend.domain.auth.repositories import RevokedTokenRepository, UnitOfWorkPort


def logout_operator(
    claims: TokenClaims,
    revoked_repo: RevokedTokenRepository,
    uow: UnitOfWorkPort,
) -> None:
    """Revoke the current token explicitly. Idempotent if jti already revoked."""
    if revoked_repo.is_revoked(claims.jti):
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
