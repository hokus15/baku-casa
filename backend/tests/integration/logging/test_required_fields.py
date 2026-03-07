from __future__ import annotations

import os

from fastapi.testclient import TestClient

from baku.backend.main import app

from ._helpers import clear_logs, find_first, logs_dir, read_json_lines


def test_json_logs_include_required_fields() -> None:
    os.environ["APP_ENV"] = "test"
    clear_logs("backend.test")

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/bootstrap",
            json={"username": "operator", "password": "Boot123!"},
        )
        assert response.status_code in (201, 409)

    rows = read_json_lines(logs_dir() / "backend.test.json.log")
    row = find_first(rows, "bootstrap_operator_completed")
    assert row is not None

    required = {
        "timestamp",
        "level",
        "logger",
        "message",
        "module",
        "funcName",
        "line",
        "correlation_id",
        "service_name",
    }
    assert required.issubset(set(row.keys()))
