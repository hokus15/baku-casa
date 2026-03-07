"""Error handlers registry — centralizes all error handler registration for the HTTP application.

All domain error handlers must be registered here and only here.

Responsibility: ERROR_HANDLERS_REGISTRATION (BootstrapInventory)
"""

from __future__ import annotations

from fastapi import FastAPI

from baku.backend.interfaces.http.error_mapper import register_error_handlers as _register_domain_error_handlers


def register_error_handlers(app: FastAPI) -> None:
    """Register all domain error handlers on the application."""
    _register_domain_error_handlers(app)
