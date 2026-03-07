from __future__ import annotations

import os

from fastapi.testclient import TestClient

from baku.backend.main import app

from ._helpers import clear_logs, logs_dir, read_text_lines


def test_logs_do_not_leak_sensitive_credentials() -> None:
    os.environ["APP_ENV"] = "test"
    clear_logs("backend.test")
    username = "operator"
    password = "SuperSecret123!"

    with TestClient(app) as client:
        client.post(
            "/api/v1/auth/bootstrap",
            json={"username": username, "password": password},
        )
        client.post(
            "/api/v1/auth/login",
            json={"username": username, "password": "WrongSecret999!"},
        )

    json_lines = read_text_lines(logs_dir() / "backend.test.json.log")
    human_lines = read_text_lines(logs_dir() / "backend.test.human.log")
    joined = "\n".join([*json_lines, *human_lines])

    assert password not in joined
    assert "WrongSecret999!" not in joined
