"""HTTP error mapper — deterministic mapping of auth domain errors to HTTP responses.

All error responses include: error_code (stable English), message (Spanish),
correlation_id (ADR-0009, constitution §III).
"""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from baku.backend.domain.auth.errors import AuthError
from baku.backend.interfaces.http.middleware.correlation_id import get_correlation_id


def _error_response(error: AuthError) -> JSONResponse:
    return JSONResponse(
        status_code=error.http_status,
        content={
            "error_code": error.error_code,
            "message": error.message,
            "correlation_id": get_correlation_id(),
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register all auth domain error handlers on the FastAPI application."""

    @app.exception_handler(AuthError)
    async def auth_error_handler(request: Request, exc: AuthError) -> JSONResponse:
        return _error_response(exc)
