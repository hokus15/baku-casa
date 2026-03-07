"""Logging context helpers and filters for EN-0200."""

from __future__ import annotations

import logging
from typing import Any

from baku.backend.interfaces.http.middleware.correlation_id import get_correlation_id


class CorrelationIdFilter(logging.Filter):
    """Inject ``correlation_id`` into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = get_correlation_id()
        return True


class ServiceNameFilter(logging.Filter):
    """Inject static service name and environment into each log record."""

    def __init__(self, service_name: str, environment: str) -> None:
        super().__init__()
        self._service_name = service_name
        self._environment = environment

    def filter(self, record: logging.LogRecord) -> bool:
        record.service_name = self._service_name
        record.environment = self._environment
        return True


def log_extra(**kwargs: Any) -> dict[str, Any]:
    """Wrap contextual key-value pairs for structured logging calls."""
    return {"extra": kwargs}
