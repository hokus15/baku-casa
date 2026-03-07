from __future__ import annotations

import logging
import os

from fastapi.testclient import TestClient

from baku.backend.infrastructure.logging.bootstrap import configure_framework_logging
from baku.backend.main import app


def test_environment_profile_is_selected_when_available() -> None:
    os.environ["APP_ENV"] = "prod"
    configure_framework_logging()

    root = logging.getLogger()
    formatters = [type(h.formatter).__name__ for h in root.handlers if h.formatter is not None]
    assert "JsonLogFormatter" in formatters

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "operator", "password": "bad-pass"},
        )
        assert response.status_code in (401, 423)
