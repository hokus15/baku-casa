"""Shared pagination helpers for v1 HTTP routers (ADR-0013).

All collection endpoints in this API version resolve pagination parameters
through this module so that the EN-0202 configuration system is the single
source of truth for defaults and limits.
"""

from __future__ import annotations

from baku.backend.infrastructure.config.pagination_settings import (
    get_pagination_settings,
)


def get_pagination_defaults() -> tuple[int, int]:
    """Return ``(default_page_size, max_page_size)`` from centralised config (ADR-0013).

    Values are validated at startup (>= 1, max >= default) by ``PaginationSettings``.
    """
    settings = get_pagination_settings()
    return settings.default_page_size, settings.max_page_size
