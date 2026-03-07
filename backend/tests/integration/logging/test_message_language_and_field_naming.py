from __future__ import annotations

import os
import re

from fastapi.testclient import TestClient

from baku.backend.main import app

from ._helpers import clear_logs, logs_dir, read_json_lines


def test_log_messages_and_keys_follow_snake_case() -> None:
    os.environ["APP_ENV"] = "test"
    clear_logs("backend.test")

    with TestClient(app) as client:
        client.post(
            "/api/v1/auth/bootstrap",
            json={"username": "operator", "password": "Boot123!"},
        )

    rows = read_json_lines(logs_dir() / "backend.test.json.log")
    assert rows

    token_re = re.compile(r"^[a-z0-9_]+$")
    key_re = re.compile(r"^[a-z][a-z0-9_]*$")
    domain_rows = [r for r in rows if str(r.get("logger", "")).startswith("baku.backend")]
    assert domain_rows

    for row in domain_rows:
        message = row.get("message")
        if isinstance(message, str):
            assert token_re.match(message)
        for key in row.keys():
            assert key_re.match(key)
