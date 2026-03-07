"""App factory — creates and fully configures the FastAPI application instance.

Single orchestration point for the bootstrap sequence. Each responsibility is
delegated to its dedicated module (BootstrapInventory, spec FR-002).

Bootstrap sequence:
  1. APP_CREATION                  — construct FastAPI instance with lifespan handler
  2. LIFESPAN_BOOTSTRAP            — delegated to lifespan.py via FastAPI lifespan arg
  3. DEPENDENCY_COMPOSITION_WIRING — wire Infrastructure -> Interfaces stubs
  4. MIDDLEWARE_REGISTRATION       — register all HTTP middleware
  5. ERROR_HANDLERS_REGISTRATION   — register all domain error handlers
  6. ROUTER_REGISTRATION           — mount all API routers

Responsibility: APP_CREATION (BootstrapInventory)
"""

from __future__ import annotations

from fastapi import FastAPI

from baku.backend.interfaces.http.bootstrap.dependency_wiring import wire_dependencies
from baku.backend.interfaces.http.bootstrap.error_handlers_registry import register_error_handlers
from baku.backend.interfaces.http.bootstrap.lifespan import lifespan
from baku.backend.interfaces.http.bootstrap.middleware_registry import register_middleware
from baku.backend.interfaces.http.bootstrap.router_registry import register_routers


def create_app() -> FastAPI:
    """Create and fully configure the FastAPI application.

    Returns a ready-to-serve FastAPI instance with all bootstrap responsibilities
    applied. The main.py entrypoint calls this function and exposes the result.
    """
    app = FastAPI(
        title="Baku Casa Backend",
        version="1.0.0",
        description="Baku Casa property management backend — MVP1",
        lifespan=lifespan,
    )
    wire_dependencies(app)
    register_middleware(app)
    register_error_handlers(app)
    register_routers(app)
    return app
