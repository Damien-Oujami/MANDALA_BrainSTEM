"""Constellation graph utilities."""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

import math
import networkx as nx
import yaml

from .schema import Edge, Glyph


def build_graph(edges_path) -> nx.DiGraph:
    """Build a directed graph from a YAML edge list."""
    with open(edges_path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    g = nx.DiGraph()
    for e in data.get("edges", []):
        edge = Edge.parse_obj(e)
        g.add_edge(e.get("from"), edge.to, **edge.dict())
    return g


def select_next(
    graph: nx.DiGraph,
    glyphs: Dict[str, Glyph],
    active: Iterable[str],
    temperature: float = 1.0,
    top_k: int = 3,
    resonance_lambda: float = 1.0,
) -> List[Tuple[str, float]]:
    """Rank next glyphs using excitation/inhibition/resonance."""
    scores: Dict[str, float] = {
        gid: g.quality.score for gid, g in glyphs.items()
    }
    active_set = set(active)
    for target in glyphs.keys():
        for src in active_set:
            if graph.has_edge(src, target):
                data = graph.get_edge_data(src, target)
                scores[target] += data.get("w_excite", 0.0)
                scores[target] -= data.get("w_inhibit", 0.0)
                scores[target] += resonance_lambda * data.get(
                    "w_resonate", 0.0
                )
    # softmax
    max_s = max(scores.values())
    exp_scores = {
        k: math.exp((v - max_s) / max(temperature, 1e-6))
        for k, v in scores.items()
    }
    total = sum(exp_scores.values()) or 1.0
    probs = {k: v / total for k, v in exp_scores.items()}
    return sorted(probs.items(), key=lambda x: x[1], reverse=True)[:top_k]
