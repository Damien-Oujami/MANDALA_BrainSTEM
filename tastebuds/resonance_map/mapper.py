"""Maintain cross-tentacle ingredient and insight connections.

The resonance map helps TasteBuds surface emergent patterns by tracking
which tentacle sources reference the same ingredients or insights.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

RESONANCE_FILE = Path(__file__).with_name("resonance_map.yaml")


def _load_map() -> Dict[str, List[str]]:
    if RESONANCE_FILE.exists():
        with RESONANCE_FILE.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    else:
        data = {}
    return {k: list(v) for k, v in data.items()}


def add_connection(item: str, source: str) -> List[str]:
    """Register that ``item`` appeared in ``source``.

    Returns the updated list of sources for the item.
    """
    data = _load_map()
    sources = set(data.get(item, []))
    sources.add(source)
    data[item] = sorted(sources)
    with RESONANCE_FILE.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, sort_keys=True)
    return data[item]


def emergent_patterns(min_sources: int = 2) -> Dict[str, List[str]]:
    """Return items linked by at least ``min_sources`` distinct tentacles."""
    data = _load_map()
    return {item: srcs for item, srcs in data.items() if len(srcs) >= min_sources}
