"""Middleware registry — centralizes all middleware registration for the HTTP application.

All middleware must be registered here and only here. Middleware is applied
before routers (registration order matters).

Responsibility: MIDDLEWARE_REGISTRATION (BootstrapInventory)
"""

from __future__ import annotations

from fastapi import FastAPI

from baku.backend.interfaces.http.middleware.correlation_id import CorrelationIdMiddleware


def register_middleware(app: FastAPI) -> None:
    """Register all HTTP middleware on the application.

    Must be called before router registration (middleware order is LIFO in Starlette).
    """
    app.add_middleware(CorrelationIdMiddleware)
