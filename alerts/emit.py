# alerts/emit.py
import time, json
from pathlib import Path

BUS = Path("alerts/events.jsonl")
BUS.parent.mkdir(parents=True, exist_ok=True)

def emit(type_, persona, topic, message, severity="medium", **context):
    evt = {
        "ts": time.time(),
        "type": type_,
        "persona": persona.upper(),
        "topic": topic,
        "severity": severity,
        "message": message,
        "context": context or {}
    }
    with BUS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt, ensure_ascii=False) + "\n")
