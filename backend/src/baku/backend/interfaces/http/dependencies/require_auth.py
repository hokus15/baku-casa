"""FastAPI dependency: require authenticated request.

Validates JWT signature + expiry, checks credential_version against DB
(global revocation on password change), and checks per-jti revocation (logout).
Raises the appropriate AuthError subclass on any failure.
"""

from __future__ import annotations

from typing import Annotated

import jwt as pyjwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from baku.backend.domain.auth.errors import (
    TokenExpired,
    TokenInvalid,
    TokenRevoked,
)
from baku.backend.infrastructure.config.auth_settings import get_auth_settings
from baku.backend.infrastructure.persistence.sqlite.auth_repositories import (
    SqliteOperatorRepository,
    SqliteRevokedTokenRepository,
)
from baku.backend.infrastructure.persistence.sqlite.db import get_session_factory
from baku.backend.infrastructure.security.jwt_service import TokenClaims, decode_token

# auto_error=False: FastAPI must NOT produce its own generic 403.
# Missing / malformed Authorization headers are caught below and raised
# as typed AuthErrors so the error mapper returns a contract-compliant body
# (error_code / Spanish message / correlation_id — ADR-0009).
_bearer = HTTPBearer(auto_error=False)


def get_current_claims(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> TokenClaims:
    """Validate bearer token and return verified TokenClaims.

    Raises TokenExpired, TokenRevoked, or TokenInvalid on failure.
    Missing Authorization header raises TokenInvalid to keep the response
    body contract-compliant instead of producing FastAPI's generic 403.
    """
    if credentials is None:
        raise TokenInvalid()

    settings = get_auth_settings()
    token = credentials.credentials

    try:
        claims = decode_token(token, settings.jwt_secret, settings.jwt_algorithm)
    except pyjwt.ExpiredSignatureError as err:
        raise TokenExpired() from err
    except pyjwt.InvalidTokenError as err:
        raise TokenInvalid() from err

    # Per-jti revocation check (logout)
    session_factory = get_session_factory()
    with session_factory() as session:
        revoked_repo = SqliteRevokedTokenRepository(session)
        if revoked_repo.is_revoked(claims.jti):
            raise TokenRevoked()

        # Global revocation check (credential_version mismatch after password change)
        op_repo = SqliteOperatorRepository(session)
        operator = op_repo.find_active()
        if operator is None or operator.credential_version != claims.ver:
            raise TokenRevoked()

    return claims
