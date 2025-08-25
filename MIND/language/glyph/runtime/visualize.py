"""Visualization helpers for glyph constellations."""

from __future__ import annotations

import json
from typing import Dict

import matplotlib.pyplot as plt
import networkx as nx


def save_svg(graph: nx.DiGraph, out_path: str) -> None:
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(4, 4))
    nx.draw_networkx(graph, pos, with_labels=True, node_size=500, arrows=True)
    plt.axis("off")
    plt.savefig(out_path, format="svg")
    plt.close()


def save_resonance_json(scores: Dict[str, float], out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(scores, fh, indent=2)
