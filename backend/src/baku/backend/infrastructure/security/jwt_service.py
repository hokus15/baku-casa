"""JWT service — stateless token issuance and validation (ADR-0005).

Claims: sub (operator_id), ver (credential_version), jti (unique token id),
        iat (issued at UTC), exp (expiry UTC).
Revocation: global via credential_version mismatch; per-token via jti lookup.

TokenClaims is defined in the application layer (application.auth.token_validator)
because it is an application-level value object.  It is re-exported here so
existing call sites that import it from jwt_service continue to work.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import jwt

from baku.backend.application.auth.token_validator import TokenClaims  # re-exported
from baku.backend.application.common.utc_clock import utcnow

__all__ = ["TokenClaims", "issue_token", "decode_token"]


def issue_token(
    operator_id: str,
    credential_version: int,
    secret: str,
    algorithm: str,
    ttl_seconds: int,
) -> tuple[str, TokenClaims]:
    """Issue a signed JWT. Returns (encoded_token, claims)."""
    now = utcnow()
    exp = now + timedelta(seconds=ttl_seconds)
    jti = str(uuid.uuid4())

    payload: dict[str, object] = {
        "sub": operator_id,
        "ver": credential_version,
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(payload, secret, algorithm=algorithm)
    claims = TokenClaims(
        sub=operator_id,
        ver=credential_version,
        jti=jti,
        iat=now,
        exp=exp,
    )
    return token, claims


def decode_token(
    token: str,
    secret: str,
    algorithm: str,
) -> TokenClaims:
    """Decode and verify JWT signature + expiry. Raises jwt.ExpiredSignatureError or
    jwt.InvalidTokenError on failure — callers must map to domain errors."""
    payload = jwt.decode(token, secret, algorithms=[algorithm])
    exp_ts: int = payload["exp"]
    iat_ts: int = payload["iat"]
    return TokenClaims(
        sub=str(payload["sub"]),
        ver=int(payload["ver"]),
        jti=str(payload["jti"]),
        iat=datetime.fromtimestamp(iat_ts, tz=timezone.utc),
        exp=datetime.fromtimestamp(exp_ts, tz=timezone.utc),
    )
