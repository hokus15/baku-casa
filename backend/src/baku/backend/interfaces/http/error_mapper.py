"""HTTP error mapper — deterministic mapping of domain errors to HTTP responses.

All error responses include: error_code (stable English), message (Spanish),
correlation_id (ADR-0009, constitution §III).
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from baku.backend.domain.auth.errors import AuthError
from baku.backend.domain.owners.errors import OwnerError, OwnerValidationError
from baku.backend.domain.properties.errors import PropertyError
from baku.backend.interfaces.http.middleware.correlation_id import (
    get_correlation_id,
)

logger = logging.getLogger(__name__)


def _json_error(
    error_code: str, message: str, http_status: int
) -> JSONResponse:
    return JSONResponse(
        status_code=http_status,
        content={
            "error_code": error_code,
            "message": message,
            "correlation_id": get_correlation_id(),
        },
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register all domain error handlers on the FastAPI application."""

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.warning(
            "request_validation_error_mapped",
            extra={
                "error_code": OwnerValidationError.error_code,
                "http_status": 400,
                "method": request.method,
                "path": str(request.url.path),
            },
        )
        return _json_error(
            OwnerValidationError.error_code, OwnerValidationError.message, 400
        )

    @app.exception_handler(AuthError)
    async def auth_error_handler(
        request: Request, exc: AuthError
    ) -> JSONResponse:
        logger.warning(
            "auth_error_mapped",
            extra={
                "error_code": exc.error_code,
                "http_status": exc.http_status,
                "method": request.method,
                "path": str(request.url.path),
            },
        )
        return _json_error(exc.error_code, exc.detail, exc.http_status)

    @app.exception_handler(OwnerError)
    async def owner_error_handler(
        request: Request, exc: OwnerError
    ) -> JSONResponse:
        logger.warning(
            "owner_error_mapped",
            extra={
                "error_code": exc.error_code,
                "http_status": exc.http_status,
                "method": request.method,
                "path": str(request.url.path),
            },
        )
        return _json_error(exc.error_code, exc.detail, exc.http_status)

    @app.exception_handler(PropertyError)
    async def property_error_handler(
        request: Request, exc: PropertyError
    ) -> JSONResponse:
        logger.warning(
            "property_error_mapped",
            extra={
                "error_code": exc.error_code,
                "http_status": exc.http_status,
                "method": request.method,
                "path": str(request.url.path),
            },
        )
        return _json_error(exc.error_code, exc.detail, exc.http_status)
