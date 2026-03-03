"""Application-layer port: JWT token issuance (ADR-0002).

Infrastructure (JwtTokenIssuer) implements this port.
Use cases depend only on this ABC — never on PyJWT directly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from baku.backend.application.auth.token_validator import TokenClaims


class TokenIssuerPort(ABC):
    @abstractmethod
    def issue(
        self,
        operator_id: str,
        credential_version: int,
        ttl_seconds: int,
    ) -> tuple[str, TokenClaims]: ...
