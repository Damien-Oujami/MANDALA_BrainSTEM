"""Utilities for loading `.glyph` YAML files into :class:`Glyph` objects."""

from __future__ import annotations

import pathlib
from typing import Iterable, List

import yaml

from .schema import Glyph


def load_glyph(path: str | pathlib.Path) -> Glyph:
    """Load and validate a single glyph file."""
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return Glyph.parse_obj(data)


def load_dir(directory: str | pathlib.Path) -> List[Glyph]:
    """Load all `.glyph` files recursively in *directory*."""
    paths: Iterable[pathlib.Path] = pathlib.Path(directory).rglob("*.glyph")
    return [load_glyph(p) for p in paths]
