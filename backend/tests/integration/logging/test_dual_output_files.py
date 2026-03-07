from __future__ import annotations

import os

from fastapi.testclient import TestClient

from baku.backend.main import app

from ._helpers import clear_logs, logs_dir, read_text_lines


def test_json_and_human_files_are_both_written() -> None:
    os.environ["APP_ENV"] = "test"
    clear_logs("backend.test")

    with TestClient(app) as client:
        client.post(
            "/api/v1/auth/bootstrap",
            json={"username": "operator", "password": "Boot123!"},
        )

    json_path = logs_dir() / "backend.test.json.log"
    human_path = logs_dir() / "backend.test.human.log"
    assert json_path.exists()
    assert human_path.exists()

    json_lines = "\n".join(read_text_lines(json_path))
    human_lines = "\n".join(read_text_lines(human_path))
    assert "bootstrap_operator_completed" in json_lines
    assert "bootstrap_operator_completed" in human_lines
