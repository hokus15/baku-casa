"""FastAPI application entry point — backend root.

Thin entrypoint: delegates all bootstrap responsibilities to the bootstrap module.

Bootstrap responsibilities (app creation, lifespan, dependency wiring, middleware,
error handlers, routers) are encapsulated in:
  baku.backend.interfaces.http.bootstrap

See: ADR-0002 (Hexagonal), ADR-0004 (HTTP/OpenAPI), ADR-0013 (fail-fast).
"""

from __future__ import annotations

from baku.backend.interfaces.http.bootstrap.app_factory import create_app

app = create_app()
