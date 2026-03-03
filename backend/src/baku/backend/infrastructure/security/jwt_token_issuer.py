"""JWT implementation of TokenIssuerPort (ADR-0002)."""

from __future__ import annotations

from baku.backend.application.auth.token_issuer_port import TokenIssuerPort
from baku.backend.application.auth.token_validator import TokenClaims
from baku.backend.infrastructure.security.jwt_service import issue_token


class JwtTokenIssuer(TokenIssuerPort):
    def __init__(self, secret: str, algorithm: str) -> None:
        self._secret = secret
        self._algorithm = algorithm

    def issue(
        self,
        operator_id: str,
        credential_version: int,
        ttl_seconds: int,
    ) -> tuple[str, TokenClaims]:
        return issue_token(
            operator_id=operator_id,
            credential_version=credential_version,
            secret=self._secret,
            algorithm=self._algorithm,
            ttl_seconds=ttl_seconds,
        )
