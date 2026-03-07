from __future__ import annotations

import os

from fastapi.testclient import TestClient

from baku.backend.main import app

from ._helpers import clear_logs, logs_dir, read_json_lines


def test_correlation_id_propagates_from_request_header() -> None:
    os.environ["APP_ENV"] = "test"
    clear_logs("backend.test")
    corr_id = "c6b7e4b6-72af-44b6-90f2-f6a3d30f77de"

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "operator", "password": "bad-pass"},
            headers={"X-Correlation-ID": corr_id},
        )
        assert response.headers.get("X-Correlation-ID") == corr_id

    rows = read_json_lines(logs_dir() / "backend.test.json.log")
    assert any(row.get("correlation_id") == corr_id for row in rows)
