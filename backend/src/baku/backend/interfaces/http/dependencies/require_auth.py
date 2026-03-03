"""FastAPI dependency: require authenticated request (ADR-0002).

This adapter depends only on the Application layer (TokenValidatorPort,
TokenClaims) and the Domain layer (AuthErrors).  No Infrastructure modules
are imported here.

The concrete TokenValidatorPort implementation (JwtTokenValidator) is wired
at the composition root in main.py via app.dependency_overrides so that the
dependency direction stays:

    Interfaces → Application ← Infrastructure
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from baku.backend.application.auth.token_validator import TokenClaims, TokenValidatorPort
from baku.backend.domain.auth.errors import TokenInvalid

# auto_error=False: FastAPI must NOT produce its own generic 403.
# Missing / malformed Authorization headers are caught below and raised
# as typed AuthErrors so the error mapper returns a contract-compliant body
# (error_code / Spanish message / correlation_id — ADR-0009).
_bearer = HTTPBearer(auto_error=False)


def get_token_validator() -> TokenValidatorPort:
    """Abstract stub — overridden at composition root via app.dependency_overrides.

    Raises NotImplementedError if called without an override in place, which
    will surface as a 500 during startup integration tests and signal a wiring
    mistake rather than silently failing.
    """
    raise NotImplementedError(
        "TokenValidatorPort not wired. "
        "Add app.dependency_overrides[get_token_validator] = get_jwt_token_validator "
        "in the composition root (main.py)."
    )


def get_current_claims(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    validator: Annotated[TokenValidatorPort, Depends(get_token_validator)],
) -> TokenClaims:
    """Validate bearer token and return verified TokenClaims.

    Raises TokenExpired, TokenRevoked, or TokenInvalid on failure.
    Missing Authorization header raises TokenInvalid to keep the response
    body contract-compliant instead of producing FastAPI's generic 403.
    """
    if credentials is None:
        raise TokenInvalid()
    return validator.validate(credentials.credentials)
