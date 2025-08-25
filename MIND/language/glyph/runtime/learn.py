"""Online learning rules for glyph constellations."""
from __future__ import annotations

import time

from .ops import clamp, ema
from .schema import Glyph


def update_resonance(
    graph,
    src: str,
    dst: str,
    alpha: float,
    sim: float,
    baseline: float = 0.0,
) -> None:
    data = graph.get_edge_data(src, dst, default={})
    w = data.get("w_resonate", 0.0)
    w = clamp(w + alpha * (sim - baseline), -1.0, 1.0)
    graph.add_edge(
        src,
        dst,
        **{**data, "w_resonate": w, "last_updated": time.time()},
    )


def update_inhibit(graph, loser: str, winner: str, beta: float) -> None:
    data = graph.get_edge_data(loser, winner, default={})
    w = data.get("w_inhibit", 0.0)
    w = clamp(w + beta, 0.0, 1.0)
    graph.add_edge(
        loser,
        winner,
        **{**data, "w_inhibit": w, "last_updated": time.time()},
    )


def reinforce_quality(glyph: Glyph, success: bool, gamma: float) -> None:
    target = 1.0 if success else 0.0
    glyph.quality.score = ema(glyph.quality.score, target, gamma)
    glyph.quality.samples += 1
