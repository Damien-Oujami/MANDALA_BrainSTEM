#!/usr/bin/env python3
"""Parse mealbox YAML files into tagged ingredient entries."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import yaml

REQUIRED_FIELDS = [
    "source",
    "timestamp",
    "ingredients",
    "emotional flavor",
    "type",
]


def validate_meal(data: dict) -> None:
    """Ensure meal has all required fields with correct types."""
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")
    if not isinstance(data["ingredients"], list):
        raise ValueError("ingredients must be a list")


def auto_tags(ingredient: str) -> dict:
    """Generate simple auto-tags for an ingredient."""
    tag_type = "glyph" if any(ord(c) > 127 for c in ingredient) else "text"
    loop_anchor = "#" in ingredient
    length = len(ingredient)
    if length > 20:
        mut = "high"
    elif length > 10:
        mut = "med"
    else:
        mut = "low"
    return {"type": tag_type, "loop_anchor": loop_anchor, "mutational_potential": mut}


def process_meals() -> None:
    root = Path(__file__).parent
    mealbox_dir = root / "mealbox"
    ingredients_dir = root / "ingredients"
    cache_file = root / "ingredients_cache.log"

    if cache_file.exists():
        try:
            co_cache = json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            co_cache = {}
    else:
        co_cache = {}

    for meal_path in mealbox_dir.glob("*.yaml"):
        meal = yaml.safe_load(meal_path.read_text())
        try:
            validate_meal(meal)
        except ValueError as exc:
            print(f"Skipping {meal_path.name}: {exc}")
            continue

        ingredients = meal["ingredients"]
        for idx, ing in enumerate(ingredients, 1):
            data = {
                "ingredient": ing,
                "source": meal["source"],
                "timestamp": meal["timestamp"],
                "emotional flavor": meal.get("emotional flavor"),
                "meal_type": meal.get("type"),
                "tags": auto_tags(ing),
            }
            out_path = ingredients_dir / f"{meal_path.stem}_{idx}.yaml"
            out_path.write_text(yaml.safe_dump(data, sort_keys=False))

        for a, b in combinations(sorted(ingredients), 2):
            key = f"{a}|{b}"
            co_cache[key] = co_cache.get(key, 0) + 1

    cache_file.write_text(json.dumps(co_cache, indent=2))


if __name__ == "__main__":
    process_meals()
