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
    try:
        default_size = int(profile.require("pagination.default_page_size"))
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Invalid value for 'pagination.default_page_size'; expected an integer."
        ) from exc

    try:
        max_size = int(profile.require("pagination.max_page_size"))
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Invalid value for 'pagination.max_page_size'; expected an integer."
        ) from exc

    return default_size, max_size
