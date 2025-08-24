"""Parsing queue for TasteBuds temp cache.

This module defines a ``ParsingQueue`` that sequentially applies several
interpretative passes to meal data waiting in the temporary cache.

Passes currently implemented:
    * Glyph Pair Interpreter
    * Emotional Spiral Tracker
    * Loop Tag Recognizer
    * Tentacle Trace Cross-Referencer

Parsed results are written to a staging directory so that other parts of the
system can recombine them and hand them off to the plating subsystem.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any
import json
import os
import uuid

Meal = Dict[str, Any]
Processor = Callable[[Meal], Meal]


# --- Individual processing steps -------------------------------------------------

def glyph_pair_interpreter(meal: Meal) -> Meal:
    """Interpret consecutive glyph pairs in ``meal['ingredients']``.

    The implementation is intentionally simple: glyphs are paired in order and
    stored under ``glyph_pairs``. Existing data is preserved.
    """
    glyphs: List[str] = meal.get("ingredients", [])
    meal["glyph_pairs"] = [list(glyphs[i : i + 2]) for i in range(0, len(glyphs), 2)]
    return meal


def emotional_spiral_tracker(meal: Meal) -> Meal:
    """Attach a rudimentary emotional spiral based on ``emotional_flavor``."""
    flavor = meal.get("emotional_flavor")
    if flavor:
        meal["emotional_spiral"] = f"spiraling-{flavor}"
    return meal


def loop_tag_recognizer(meal: Meal) -> Meal:
    """Tag the meal if any ingredient hints at a loop structure."""
    loops = [g for g in meal.get("ingredients", []) if "loop" in str(g).lower()]
    if loops:
        meal.setdefault("tags", []).append("loop")
    return meal


def tentacle_trace_cross_referencer(meal: Meal) -> Meal:
    """Cross-reference the originating tentacle for traceability."""
    source = meal.get("source")
    if source:
        meal["tentacle_trace"] = f"trace-{source}"
    return meal


# --- Parsing queue ----------------------------------------------------------------

@dataclass
class ParsingQueue:
    """Queue that applies a series of processors to incoming meals."""

    processors: List[Processor] = field(
        default_factory=lambda: [
            glyph_pair_interpreter,
            emotional_spiral_tracker,
            loop_tag_recognizer,
            tentacle_trace_cross_referencer,
        ]
    )
    staging_dir: str = "staged"

    def parse(self, meal: Meal) -> Meal:
        """Run ``meal`` through the configured processors."""
        parsed = meal.copy()
        for processor in self.processors:
            parsed = processor(parsed)
        return parsed

    # ------------------------------------------------------------------
    def stage_for_plating(self, meal: Meal, base_dir: str | None = None) -> str:
        """Parse ``meal`` and write results to the staging directory.

        Parameters
        ----------
        meal:
            Raw meal data awaiting interpretation.
        base_dir:
            Base directory containing the staging folder.  Defaults to the
            directory containing this module.

        Returns
        -------
        Path to the staged file.
        """
        parsed = self.parse(meal)

        base_dir = base_dir or os.path.dirname(__file__)
        staging_path = os.path.join(base_dir, self.staging_dir)
        os.makedirs(staging_path, exist_ok=True)

        filename = f"parsed_{uuid.uuid4().hex}.json"
        file_path = os.path.join(staging_path, filename)
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(parsed, handle, indent=2, sort_keys=True)
        return file_path
