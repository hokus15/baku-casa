"""Use case: Logout operator — persist RevokedToken for current jti.

Creates a RevokedToken with reason=logout so the jti cannot be reused.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from baku.backend.application.common.utc_clock import utcnow
from baku.backend.domain.auth.entities import RevocationReason, RevokedToken
from baku.backend.infrastructure.persistence.sqlite.auth_repositories import (
    SqliteRevokedTokenRepository,
)
from baku.backend.infrastructure.security.jwt_service import TokenClaims


def logout_operator(claims: TokenClaims, session: Session) -> None:
    """Revoke the current token explicitly. Idempotent if jti already revoked."""
    revoked_repo = SqliteRevokedTokenRepository(session)

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
    session.commit()
