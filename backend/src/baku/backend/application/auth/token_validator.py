"""Application-layer token validation port (ADR-0002).

TokenClaims is defined here — not in Infrastructure — because it is the
value object exchanged between the authentication use cases and the HTTP
adapter. Infrastructure (JwtTokenValidator) implements the port; the
adapter depends only on this module.

Dependency direction:   Interfaces → Application ← Infrastructure
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenClaims:
    """Decoded, verified JWT payload carried through the application layer."""

    sub: str  # operator_id
    ver: int  # credential_version — used for global revocation after password change
    jti: str  # unique token id — used for per-token revocation (logout)
    iat: datetime
    exp: datetime


class TokenValidatorPort(ABC):
    """Port: validate a raw bearer token string.

    Implementations must:
    - verify JWT signature and expiry
    - check per-jti revocation (logout)
    - check credential_version against the active operator (global revocation)

    Raises:
        TokenExpired   — token has expired
        TokenRevoked   — token was explicitly revoked (logout or password change)
        TokenInvalid   — token is structurally invalid / signature mismatch
    """

    @abstractmethod
    def validate(self, token: str) -> TokenClaims: ...
