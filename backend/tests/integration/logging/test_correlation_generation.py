from __future__ import annotations

import os
import re

from fastapi.testclient import TestClient

from baku.backend.main import app

from ._helpers import clear_logs, logs_dir, read_json_lines


def test_correlation_id_is_generated_when_missing() -> None:
    os.environ["APP_ENV"] = "test"
    clear_logs("backend.test")

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "operator", "password": "bad-pass"},
        )

    corr_id = response.headers.get("X-Correlation-ID")
    assert corr_id is not None
    assert re.match(
        r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
        corr_id,
    )

    rows = read_json_lines(logs_dir() / "backend.test.json.log")
    assert any(row.get("correlation_id") == corr_id for row in rows)
