"""FastAPI application entry point — backend root."""
from __future__ import annotations

from fastapi import FastAPI

from baku.backend.interfaces.http.api.v1.auth_router import router as auth_router
from baku.backend.interfaces.http.error_mapper import register_error_handlers
from baku.backend.interfaces.http.middleware.correlation_id import CorrelationIdMiddleware

app = FastAPI(
    title="Baku Casa Backend",
    version="1.0.0",
    description="Baku Casa property management backend — MVP1",
)

# Middleware (registered before routes)
app.add_middleware(CorrelationIdMiddleware)

# Error handlers
register_error_handlers(app)

# Routers
app.include_router(auth_router)
