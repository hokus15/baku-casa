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

    # Explicitly validate required claims and types so callers only see
    # jwt.InvalidTokenError / jwt.ExpiredSignatureError, never raw KeyError/TypeError.
    try:
        raw_exp = payload["exp"]
        raw_iat = payload["iat"]
        raw_sub = payload["sub"]
        raw_ver = payload["ver"]
        raw_jti = payload["jti"]
    except KeyError as exc:
        # Normalize missing-claim errors to InvalidTokenError so upstream
        # error mapping remains consistent (e.g. AUTH_TOKEN_INVALID).
        claim_name = exc.args[0] if exc.args else "unknown"
        raise jwt.InvalidTokenError(f"Missing required claim: {claim_name}") from exc

    try:
        exp_ts = int(raw_exp)
        iat_ts = int(raw_iat)
        ver = int(raw_ver)
    except (TypeError, ValueError) as exc:
        raise jwt.InvalidTokenError("Invalid claim type in token payload") from exc

    try:
        iat_dt = datetime.fromtimestamp(iat_ts, tz=timezone.utc)
        exp_dt = datetime.fromtimestamp(exp_ts, tz=timezone.utc)
    except (OSError, OverflowError, ValueError) as exc:
        raise jwt.InvalidTokenError("Invalid timestamp in token claims") from exc

    return TokenClaims(
        sub=str(raw_sub),
        ver=ver,
        jti=str(raw_jti),
        iat=iat_dt,
        exp=exp_dt,
    )
