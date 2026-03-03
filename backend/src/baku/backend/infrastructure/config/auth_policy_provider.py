"""AuthSettings implementation of AuthPolicyPort (ADR-0002)."""

from __future__ import annotations

from baku.backend.application.auth.auth_policy_port import AuthPolicyPort
from baku.backend.infrastructure.config.auth_settings import get_auth_settings


class AuthSettingsPolicy(AuthPolicyPort):
    @property
    def token_ttl_seconds(self) -> int:
        return get_auth_settings().token_ttl_seconds

    @property
    def max_failed_attempts(self) -> int:
        return get_auth_settings().max_failed_attempts

    @property
    def lockout_minutes(self) -> int:
        return get_auth_settings().lockout_minutes
