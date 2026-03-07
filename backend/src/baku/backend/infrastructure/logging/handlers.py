"""Custom logging handlers for EN-0200."""

from __future__ import annotations

import time
from datetime import UTC, datetime, timedelta, tzinfo
from logging.handlers import TimedRotatingFileHandler
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class MadridTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Rotate at midnight Europe/Madrid while keeping event timestamps in UTC."""

    _tz: tzinfo
    try:
        _tz = ZoneInfo("Europe/Madrid")
    except ZoneInfoNotFoundError:
        # On Windows CI/dev without tzdata installed, degrade safely to UTC.
        _tz = UTC

    def computeRollover(self, currentTime: int) -> int:  # noqa: N802
        current_dt = datetime.fromtimestamp(currentTime, tz=self._tz)
        next_midnight = current_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if next_midnight <= current_dt:
            next_midnight = next_midnight + timedelta(days=1)
        return int(next_midnight.timestamp())

    def shouldRollover(self, record) -> int:  # type: ignore[override]
        if self.stream is None:
            self.stream = self._open()
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0
