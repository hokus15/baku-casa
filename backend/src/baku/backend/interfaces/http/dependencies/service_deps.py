"""Abstract dependency stubs: per-request service instances (ADR-0002).

Concrete implementations are provided by infrastructure via
app.dependency_overrides in the composition root (main.py).
"""

from __future__ import annotations

from baku.backend.application.auth.auth_policy_port import AuthPolicyPort
from baku.backend.application.auth.password_hasher_port import PasswordHasherPort
from baku.backend.application.auth.token_issuer_port import TokenIssuerPort


def get_password_hasher() -> PasswordHasherPort:
    raise NotImplementedError(
        "get_password_hasher not wired — add app.dependency_overrides[get_password_hasher] in main.py"
    )


def get_token_issuer() -> TokenIssuerPort:
    raise NotImplementedError("get_token_issuer not wired — add app.dependency_overrides[get_token_issuer] in main.py")


def get_auth_policy() -> AuthPolicyPort:
    raise NotImplementedError("get_auth_policy not wired — add app.dependency_overrides[get_auth_policy] in main.py")
