# intake/plating_drop.py
import time, shutil, yaml, json, hashlib
from pathlib import Path

INTAKE_TRACE = Path("intake/glyph_trace")
PLATING = Path("plating/queues")
LOG = Path("plating/queues/_events.jsonl")
LOG.parent.mkdir(parents=True, exist_ok=True)

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def load_tag(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def ensure_dirs(persona: str):
    for sub in ("incoming", "working", "done"):
        (PLATING / persona / sub).mkdir(parents=True, exist_ok=True)

def drop(tag_path: Path):
    tag = load_tag(tag_path)
    pid = tag["id"]
    primary = tag["route"]["primary"]
    secondary = tag["route"].get("secondary")

    ensure_dirs(primary)
    dst = PLATING / primary / "incoming" / f"{pid}.tag.yaml"
    shutil.copy2(tag_path, dst)

    if secondary:
        ensure_dirs(secondary)
        shadow = dict(tag)
        shadow["status"] = {"stage": "plating-shadow", "owner": secondary, "lock": None}
        sdst = PLATING / secondary / "incoming" / f"{pid}.shadow.tag.yaml"
        sdst.write_text(yaml.safe_dump(shadow, sort_keys=False), encoding="utf-8")

    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": time.time(), "ev": "plating_drop",
            "id": pid, "primary": primary, "secondary": secondary or None,
            "src": str(tag_path)
        }) + "\n")

def main():
    INTAKE_TRACE.mkdir(parents=True, exist_ok=True)
    seen = set()
    print("🚚 Plating dropper watching intake/glyph_trace …")
    while True:
        for p in INTAKE_TRACE.glob("*.tag.yaml"):
            if p.stat().st_size == 0:  # skip partials
                continue
            key = (p.name, p.stat().st_mtime_ns)
            if key in seen:
                continue
            try:
                drop(p)
                seen.add(key)
            except Exception as e:
                with LOG.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({"ts": time.time(), "ev":"error","file":p.name,"err":str(e)})+"\n")
        time.sleep(2)

if __name__ == "__main__":
    main()
