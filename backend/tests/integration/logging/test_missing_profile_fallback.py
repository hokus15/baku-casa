from __future__ import annotations

import logging
import os
from pathlib import Path

from baku.backend.infrastructure.logging.bootstrap import configure_framework_logging


def _profile_path(name: str) -> Path:
    return Path(__file__).resolve().parents[3] / f"logging.{name}.ini"


def test_missing_profile_activates_safe_fallback() -> None:
    os.environ["APP_ENV"] = "test"
    profile = _profile_path("test")
    backup = profile.with_suffix(".ini.bak")
    profile.rename(backup)
    try:
        configure_framework_logging()
        root = logging.getLogger()
        assert any(isinstance(h, logging.StreamHandler) for h in root.handlers)
    finally:
        backup.rename(profile)
