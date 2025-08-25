"""Quality and confidence helpers."""

from __future__ import annotations

from .ops import ema
from .schema import Quality


def update_quality(q: Quality, value: float, gamma: float) -> None:
    """EMA update of a quality score."""
    q.score = ema(q.score, value, gamma)
    q.samples += 1
