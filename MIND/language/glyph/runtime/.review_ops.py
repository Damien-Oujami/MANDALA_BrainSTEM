"""Definition of glyph operation helpers used by the execution engine."""

from __future__ import annotations

from typing import Any, Dict
from types import SimpleNamespace

# ---------------------------------------------------------------------------
# Expression helpers
# ---------------------------------------------------------------------------


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def ema(prev: float, new: float, alpha: float) -> float:
    return (1 - alpha) * prev + alpha * new


SAFE_FUNCS = {
    "min": min,
    "max": max,
    "abs": abs,
    "clamp": clamp,
    "ema": ema,
}


def _to_ns(obj: Any) -> Any:
    """Recursively convert mappings to allow attribute access."""
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: _to_ns(v) for k, v in obj.items()})
    return obj


def evaluate(expr: str, env: Dict[str, Any]) -> Any:
    """Evaluate *expr* using a tiny, safe environment."""
    ns_env = {k: _to_ns(v) for k, v in env.items()}
    return eval(expr, {"__builtins__": {}}, {**SAFE_FUNCS, **ns_env})


# ---------------------------------------------------------------------------
# Dot path helpers
# ---------------------------------------------------------------------------

def get_path(obj: Dict[str, Any], path: str) -> Any:
    for part in path.split("."):
        if not isinstance(obj, dict):
            return None
        obj = obj.get(part, {})
    return obj


def set_path(obj: Dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    for part in parts[:-1]:
        obj = obj.setdefault(part, {})
    obj[parts[-1]] = value


# ---------------------------------------------------------------------------
# Operation implementations
# ---------------------------------------------------------------------------

def op_filter(step: Dict[str, Any], env: Dict[str, Any]) -> bool:
    keep_if = step.get("with", {}).get("keep_if", "True")
    return bool(evaluate(keep_if, env))


def op_set(step: Dict[str, Any], env: Dict[str, Any]) -> None:
    key = step["with"].get("key")
    value = evaluate(step["with"].get("value", "None"), env)
    set_path(env, key, value)


def op_map(step: Dict[str, Any], env: Dict[str, Any]) -> None:
    src = step["with"].get("from")
    dst = step["with"].get("to")
    using = step["with"].get("using", "x")
    x = get_path(env, src)
    value = evaluate(using, {**env, "x": x})
    set_path(env, dst, value)


def op_score(step: Dict[str, Any], env: Dict[str, Any]) -> None:
    persona = step["with"].get("persona")
    delta = evaluate(str(step["with"].get("delta", 0)), env)
    personas = env.setdefault("personas", {})
    personas[persona] = personas.get(persona, 0.0) + delta


def op_route(step: Dict[str, Any], env: Dict[str, Any]) -> None:
    to = step["with"].get("to")
    env.setdefault("routes", []).append(to)


def op_emit(step: Dict[str, Any], env: Dict[str, Any]) -> None:
    key = step["with"].get("key")
    value = evaluate(step["with"].get("value", "None"), env)
    env.setdefault("outputs", {})[key] = value


def op_call(step: Dict[str, Any], env: Dict[str, Any]) -> None:
    # Placeholder for future policy invocation.
    pass


def op_halt(step: Dict[str, Any], env: Dict[str, Any]) -> str:
    return "halt"


OP_HANDLERS = {
    "filter": op_filter,
    "set": op_set,
    "map": op_map,
    "score": op_score,
    "route": op_route,
    "emit": op_emit,
    "call": op_call,
    "halt": op_halt,
}
