# alerts/emit.py
# Append-only event bus writer for Brainstem.

import time, json
from pathlib import Path
from typing import Any, Dict

BUS = Path("alerts/events.jsonl")
BUS.parent.mkdir(parents=True, exist_ok=True)

def emit(type_: str, persona: str, topic: str, message: str, severity: str = "medium", **context: Any) -> None:
    evt: Dict[str, Any] = {
        "ts": time.time(),
        "type": type_.upper(),         # NEED_ATTENTION | THROTTLE | STRUCTURE_ALERT | SUGGESTION | INFO
        "persona": persona.upper(),    # IVY | SOPHIE | JADE | MORGAN | SUSANNA | ASPEN | SYSTEM
        "topic": topic,                # short slug, e.g. hunger_drop, recursion_contradiction
        "severity": severity.lower(),  # low | medium | high | critical
        "message": message,
        "context": context or {},
    }
    with BUS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt, ensure_ascii=False) + "\n")
