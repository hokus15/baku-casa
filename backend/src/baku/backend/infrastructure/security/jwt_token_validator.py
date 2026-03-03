"""Concrete token validator — infrastructure implementation of TokenValidatorPort.

Wires together PyJWT, auth settings, and SQLite repositories to satisfy the
application port.  The only file in the infrastructure layer that should be
imported by the composition root (main.py) for the dependency override.

Dependency direction (ADR-0002):
    Infrastructure → Application (port + TokenClaims)
    Infrastructure → Domain    (typed errors)
"""

from __future__ import annotations

import jwt as pyjwt

from baku.backend.application.auth.token_validator import TokenClaims, TokenValidatorPort
from baku.backend.domain.auth.errors import TokenExpired, TokenInvalid, TokenRevoked
from baku.backend.infrastructure.config.auth_settings import get_auth_settings
from baku.backend.infrastructure.persistence.sqlite.auth_repositories import (
    SqliteOperatorRepository,
    SqliteRevokedTokenRepository,
)
from baku.backend.infrastructure.persistence.sqlite.db import get_session_factory
from baku.backend.infrastructure.security.jwt_service import decode_token


class JwtTokenValidator(TokenValidatorPort):
    """Validate a signed JWT against the current auth settings and SQLite revocation store."""

    def validate(self, token: str) -> TokenClaims:
        settings = get_auth_settings()

        try:
            claims = decode_token(token, settings.jwt_secret, settings.jwt_algorithm)
        except pyjwt.ExpiredSignatureError as err:
            raise TokenExpired() from err
        except pyjwt.InvalidTokenError as err:
            raise TokenInvalid() from err

        session_factory = get_session_factory()
        with session_factory() as session:
            # Per-token revocation check (logout path)
            revoked_repo = SqliteRevokedTokenRepository(session)
            if revoked_repo.is_revoked(claims.jti):
                raise TokenRevoked()

            # Global revocation check (credential_version mismatch after password change)
            op_repo = SqliteOperatorRepository(session)
            operator = op_repo.find_active()
            if operator is None or operator.credential_version != claims.ver:
                raise TokenRevoked()

        return claims


def get_jwt_token_validator() -> TokenValidatorPort:
    """FastAPI dependency factory — returns a JwtTokenValidator instance.

    Registered at the composition root (main.py) via app.dependency_overrides.
    """
    return JwtTokenValidator()
