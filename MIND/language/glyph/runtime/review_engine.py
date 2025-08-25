"""Minimal execution engine for glyphs."""

from __future__ import annotations

import argparse
import pathlib
from typing import Dict, Iterable

from .loader import load_glyph
from .ops import OP_HANDLERS, evaluate
from .schema import Glyph


def execute(glyph: Glyph, ctx: Dict) -> Dict:
    """Execute *glyph* against *ctx* and return the mutated context."""
    env = ctx
    for step in glyph.ops.steps:
        if step.if_ and not evaluate(step.if_, env):
            continue
        handler = OP_HANDLERS[step.do]
        result = handler(step.model_dump(by_alias=True), env)
        if result == "halt":
            break
        eval_env = {**env, **env.get("outputs", {})}
        try:
            stop = any(evaluate(cond, eval_env) for cond in glyph.option_stop)
        except NameError:
            stop = False
        if stop:
            break
    return env


def _load_manifest(path: pathlib.Path) -> Dict[str, Glyph]:
    import yaml

    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    glyphs = {
        g["id"]: load_glyph(g["path"]) for g in data.get("glyphs", [])
    }
    return glyphs


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=pathlib.Path, required=True)
    parser.add_argument("--steps", type=int, default=1)
    args = parser.parse_args(list(argv) if argv is not None else None)

    glyphs = _load_manifest(args.manifest)
    ctx: Dict = {
        "memory": {"heat": 0.0, "loops": {"anchor": 0.0}, "alignment": 0.0},
        "context": {"loop": {"seen": 1}, "alignment": 0.8},
        "intent": {"strength": 0.5},
        "outputs": {},
        "routes": [],
    }

    current = next(iter(glyphs.values()))
    for _ in range(args.steps):
        ctx = execute(current, ctx)
        print(f"executed {current.id} -> routes={ctx.get('routes')}")
        if not ctx.get("routes"):
            break
        nxt = ctx["routes"].pop(0)
        current = glyphs.get(nxt, current)


if __name__ == "__main__":
    main()
