"""Logging formatters for EN-0200 structured output."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

_RESERVED_KEYS = {
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
    "message",
    "asctime",
}


class JsonLogFormatter(logging.Formatter):
    """Render each log record as one JSON object line."""

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat().replace("+00:00", "Z")
        payload: dict[str, object] = {
            "timestamp": ts,
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "func_name": record.funcName,
            "line": record.lineno,
            "service_name": getattr(record, "service_name", "baku-backend"),
            "environment": getattr(record, "environment", "dev"),
            "correlation_id": getattr(record, "correlation_id", ""),
            "message": record.getMessage(),
        }

        # Preserve contextual key-value fields as structured output.
        for key, value in record.__dict__.items():
            if key not in _RESERVED_KEYS and key not in payload:
                payload[key] = value

        if record.exc_info:
            payload["error_type"] = record.exc_info[0].__name__ if record.exc_info[0] else "Exception"
            payload["error_message"] = str(record.exc_info[1]) if record.exc_info[1] else ""

        return json.dumps(payload, ensure_ascii=True)
