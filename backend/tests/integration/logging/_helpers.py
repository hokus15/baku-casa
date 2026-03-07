from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def backend_root() -> Path:
    return Path(__file__).resolve().parents[3]


def logs_dir() -> Path:
    path = backend_root() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def clear_logs(prefix: str) -> None:
    for p in logs_dir().glob(f"{prefix}*"):
        p.unlink(missing_ok=True)


def read_json_lines(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def read_text_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def find_first(rows: list[dict[str, Any]], message: str) -> dict[str, Any] | None:
    for row in rows:
        if row.get("message") == message:
            return row
    return None
