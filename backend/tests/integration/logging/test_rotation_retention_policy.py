from __future__ import annotations

import logging
import os
from pathlib import Path

from fastapi.testclient import TestClient

from baku.backend.main import app

from ._helpers import clear_logs, logs_dir, read_text_lines


def test_rollover_preserves_events_before_and_after_rotation() -> None:
    os.environ["APP_ENV"] = "test"
    clear_logs("backend.test")

    with TestClient(app):
        logger = logging.getLogger("integration.rotation")
        logger.info("rotation_before_marker")

        rollover_handlers = [h for h in logging.getLogger().handlers if hasattr(h, "doRollover")]
        assert rollover_handlers
        for handler in rollover_handlers:
            handler.doRollover()

        logger.info("rotation_after_marker")

    all_content: list[str] = []
    for p in logs_dir().glob("backend.test*.log*"):
        all_content.extend(read_text_lines(Path(p)))
    joined = "\n".join(all_content)

    assert "rotation_before_marker" in joined
    assert "rotation_after_marker" in joined
