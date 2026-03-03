"""Correlation ID middleware — extracts or generates per-request correlation_id.

Per constitution §Invariants: correlation_id MUST propagate between input,
processing and outgoing integration.
"""
from __future__ import annotations

import uuid
from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

_CORRELATION_ID_CTX: ContextVar[str] = ContextVar("correlation_id", default="")

HEADER_NAME = "X-Correlation-ID"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        correlation_id = request.headers.get(HEADER_NAME) or str(uuid.uuid4())
        token = _CORRELATION_ID_CTX.set(correlation_id)
        try:
            response: Response = await call_next(request)
            response.headers[HEADER_NAME] = correlation_id
            return response
        finally:
            _CORRELATION_ID_CTX.reset(token)


def get_correlation_id() -> str:
    """Return current request correlation_id, or generate a new one if not set."""
    value = _CORRELATION_ID_CTX.get()
    return value if value else str(uuid.uuid4())
