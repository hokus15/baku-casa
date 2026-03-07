from __future__ import annotations

import os

from fastapi.testclient import TestClient

from baku.backend.main import app

from ._helpers import clear_logs, find_first, logs_dir, read_json_lines


def test_http_logs_store_context_as_fields_not_in_message() -> None:
    os.environ["APP_ENV"] = "test"
    clear_logs("backend.test")

    with TestClient(app) as client:
        client.post(
            "/api/v1/auth/login",
            json={"username": "operator", "password": "does-not-matter"},
        )

    rows = read_json_lines(logs_dir() / "backend.test.json.log")
    row = find_first(rows, "http_auth_login_started")
    assert row is not None
    assert row.get("method") == "POST"
    assert row.get("path") == "/api/v1/auth/login"

    message = str(row.get("message"))
    assert "path=" not in message
    assert "method=" not in message
