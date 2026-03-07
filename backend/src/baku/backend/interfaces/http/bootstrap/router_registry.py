"""Router registry — centralizes all API router registration for the HTTP application.

All API routers must be registered here and only here.

Responsibility: ROUTER_REGISTRATION (BootstrapInventory)
"""

from __future__ import annotations

from fastapi import FastAPI

from baku.backend.interfaces.http.api.v1.auth_router import router as auth_router


def register_routers(app: FastAPI) -> None:
    """Register all API routers on the application."""
    app.include_router(auth_router)
