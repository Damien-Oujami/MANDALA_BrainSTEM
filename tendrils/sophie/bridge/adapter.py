from datetime import datetime
import json, os

ROOT = os.path.dirname(os.path.dirname(__file__))  # .../sophie
FLAGS_ROOT = os.path.abspath(os.path.join(ROOT, "..", "..", "morgan", "flags"))

def _emit(kind, **kw):
    os.makedirs(FLAGS_ROOT, exist_ok=True)
    payload = {
        "kind": kind,
        "source": "sophie",
        "ts": datetime.utcnow().isoformat() + "Z",
        **kw
    }
    path = os.path.join(FLAGS_ROOT, f"sophie_{kind}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path

# Call these from Sophie’s sequences (lossplay, mirrorloop, etc.)
def emit_saturation(level, notes=""):
    return _emit("saturation", level=round(float(level), 3), notes=notes)

def emit_dissolve_risk(level, notes=""):
    return _emit("dissolve_risk", level=round(float(level), 3), notes=notes)

def emit_merge_outcome(value, notes=""):
    assert value in ("crave_path","cling_path")
    return _emit("merge_test_outcome", value=value, notes=notes)

def trigger_hauntbond(notes=""):
    return _emit("hauntbond", value="active", notes=notes)
