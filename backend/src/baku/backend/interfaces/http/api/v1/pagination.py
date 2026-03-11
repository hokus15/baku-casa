"""Shared pagination helpers for v1 HTTP routers (ADR-0013).

All collection endpoints in this API version resolve pagination parameters
through this module so that the EN-0202 configuration system is the single
source of truth for defaults and limits.
"""

from __future__ import annotations

from baku.backend.infrastructure.config.runtime_settings import (
    RuntimeConfigurationProvider,
)


def get_pagination_defaults() -> tuple[int, int]:
    """Return ``(default_page_size, max_page_size)`` from centralised config (ADR-0013)."""
    profile = RuntimeConfigurationProvider().get_profile()
    default_size = int(
        profile.values.get("pagination.default_page_size", "20")
    )
    max_size = int(profile.values.get("pagination.max_page_size", "100"))
    return default_size, max_size
