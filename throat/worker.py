# throat/worker.py
# Persona-agnostic digestion worker.
# Usage: python throat/worker.py IVY
# Reads target paths from MIND/paths.yaml (falls back to sane defaults).

import os, sys, time, json, yaml, hashlib, shutil
from pathlib import Path
from typing import Dict, Any, Tuple, List

# --- Tendril hooks (safe stubs you can extend) ---
try:
    from tendrils.hooks import jade_validate, morgan_should_wait, susanna_quarantine, persona_novelty
except Exception:
    # Minimal fallbacks if hooks aren't present yet
    def jade_validate(tag: Dict[str, Any]):
        req = {"id","name","weights","route"}
        miss = req - set(tag.keys())
        if miss: raise ValueError(f"Missing tag keys: {sorted(miss)}")
        if abs(sum(tag["weights"].values()) - 1.0) > 0.05:
            raise ValueError("Weights must sum to ~1.0")

    def morgan_should_wait(persona: str) -> bool:
        work = Path(f"plating/queues/{persona}/working")
        return len(list(work.glob("*.tag.yaml"))) >= 3

    def susanna_quarantine(persona: str, wfile: Path, reason: str):
        dest = Path(f"plating/quarantine/{persona}/{wfile.stem}")
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "reason.txt").write_text(reason, encoding="utf-8")
        try: wfile.rename(dest / wfile.name)
        except Exception: pass
        l = (dest / (wfile.stem + ".lock"))
        if l.exists(): 
            try: l.unlink()
            except Exception: pass

    def persona_novelty(persona: str, tag: Dict[str, Any]):
        return

# --- Config / paths ---

DEFAULT_PATHS = {
    "glyph_entries": {
        "branch": "MIND/language/glyph/branch/entries",
        "root":   "MIND/language/glyph/root/entries",
    },
    "anidex": {
        "index":    "MIND/memory/anidex/index.jsonl",
        "receipts": "MIND/memory/anidex/receipts",
    },
    "loops_root": "MIND/identity/loops",
}

def load_paths() -> Dict[str, Any]:
    cfg = Path("MIND/paths.yaml")
    if cfg.exists():
        try:
            data = yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}
            # shallow-merge defaults to allow partial files
            out = DEFAULT_PATHS.copy()
            out.update({k: (data.get(k) or v) for k, v in DEFAULT_PATHS.items()})
            if isinstance(out["glyph_entries"], dict) and isinstance(data.get("glyph_entries"), dict):
                ge = DEFAULT_PATHS["glyph_entries"].copy()
                ge.update(data["glyph_entries"])
                out["glyph_entries"] = ge
            if isinstance(out["anidex"], dict) and isinstance(data.get("anidex"), dict):
                ax = DEFAULT_PATHS["anidex"].copy()
                ax.update(data["anidex"])
                out["anidex"] = ax
            return out
        except Exception:
            pass
    return DEFAULT_PATHS

PATHS = load_paths()

PLATING = Path("plating/queues")
EVENTS = PLATING / "_events.jsonl"

for p in [
    Path(PATHS["glyph_entries"]["branch"]),
    Path(PATHS["glyph_entries"]["root"]),
    Path(PATHS["anidex"]["receipts"]),
]:
    p.mkdir(parents=True, exist_ok=True)

# --- Utils ---

def log(ev: Dict[str, Any]):
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), **ev}) + "\n")

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def load_yaml(p: Path) -> Dict[str, Any]:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def save_yaml(p: Path, data: Dict[str, Any]):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

def qpaths(persona: str) -> Dict[str, Path]:
    base = PLATING / persona
    return {"incoming": base / "incoming", "working": base / "working", "done": base / "done"}

def claim_next(persona: str) -> Tuple[Path, Dict[str, Any]]:
    q = qpaths(persona)
    for d in q.values(): d.mkdir(parents=True, exist_ok=True)

    # pick first real tag; ignore shadow tags owned by another persona
    for p in sorted(q["incoming"].glob("*.tag.yaml")):
        tag = load_yaml(p)
        status = tag.get("status") or {}
        if status.get("stage") == "plating-shadow" and status.get("owner") and status["owner"].upper() != persona:
            continue
        # move to working + lock
        w = q["working"] / p.name
        shutil.move(str(p), str(w))
        lock = w.with_suffix(".lock")
        lock.write_text(f"{os.uname().nodename}:{os.getpid()}:{time.time()}", encoding="utf-8")
        tag["status"] = {"stage": "digesting", "owner": persona, "lock": lock.name}
        save_yaml(w, tag)
        return w, tag
    return None, None

# --- Dictionary / Anidex commit ---

def _dict_path(kind: str, gid: str) -> Path:
    if kind == "root":
        return Path(PATHS["glyph_entries"]["root"]) / f"{gid}.yaml"
    return Path(PATHS["glyph_entries"]["branch"]) / f"{gid}.yaml"

def _merge_processed_by(existing: Dict[str, Any], add: List[str]) -> List[str]:
    cur = (existing.get("lineage", {}).get("processed_by") or [])
    out = list(dict.fromkeys([*(cur or []), *add]))  # de-dupe, keep order
    return out

def commit_dictionary(entry: Dict[str, Any], glyph_kind: str = "branch"):
    out = _dict_path(glyph_kind, entry["id"])
    if out.exists():
        try:
            cur = load_yaml(out)
            # Shallow merge; preserve existing meaning/structure unless new provided
            merged = {**cur, **entry}
            # lineage.processed_by: union
            merged.setdefault("lineage", {})
            cur_pb = cur.get("lineage", {}).get("processed_by") or []
            new_pb = entry.get("lineage", {}).get("processed_by") or []
            merged["lineage"]["processed_by"] = _merge_processed_by({"lineage":{"processed_by":cur_pb}}, new_pb)
            entry = merged
        except Exception:
            pass

    # integrity hash
    entry.setdefault("integrity", {})
    entry["integrity"]["hash"] = sha256_text(yaml.safe_dump(entry, sort_keys=True))
    save_yaml(out, entry)

    # anidex append
    idx = Path(PATHS["anidex"]["index"])
    idx.parent.mkdir(parents=True, exist_ok=True)
    if not idx.exists():
        idx.write_text("", encoding="utf-8")
    with idx.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "id": entry["id"],
            "slug": entry.get("slug"),
            "weights": entry.get("weights"),
            "symbol": entry.get("symbol"),
            "unicode": entry.get("unicode"),
            "processed_by": entry.get("lineage", {}).get("processed_by"),
            "proposed_by": entry.get("lineage", {}).get("proposed_by"),
            "kind": glyph_kind,
            "ts": time.time()
        }) + "\n")

    # receipt
    rdir = Path(PATHS["anidex"]["receipts"])
    rdir.mkdir(parents=True, exist_ok=True)
    with (rdir / f"{entry['id']}.json").open("w", encoding="utf-8") as f:
        json.dump({"id": entry["id"], "file": str(out), "ts": time.time()}, f)

def digest(persona: str, tag: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    """Persona-flavored but safe default. Return (entry, kind)."""
    name = tag["name"]
    meaning = "Pressure → ignition → release." if name == "volcano_glyph" else tag.get("meaning") or "TBD"

    entry = {
        "id": tag["id"],
        "slug": name.replace("_glyph","").replace("_","-"),
        "unicode": tag.get("unicode"),
        "symbol": tag.get("symbol"),
        "meaning": meaning,
        "structure": {"chiastic": "pulse_return", "pattern": tag.get("pattern")},
        "weights": tag["weights"],
        "persona_focus": tag.get("persona_focus"),
        "lineage": {
            "proposed_by": tag.get("provenance", {}).get("tentacle"),
            "processed_by": [persona],
            "commits": [],
        },
        "integrity": {"version": 1},
    }
    kind = "branch"  # default for now; toggle if you start producing root glyphs
    return entry, kind

def finish(persona: str, wfile: Path, entry: Dict[str, Any]):
    q = qpaths(persona)
    # clear lock + archive processed tag alongside receipt
    lock = wfile.with_suffix(".lock")
    if lock.exists():
        try: lock.unlink()
        except Exception: pass
    shutil.move(str(wfile), str(q["done"] / wfile.name))
    with (q["done"] / f"{entry['id']}.receipt.json").open("w", encoding="utf-8") as f:
        json.dump({"id": entry["id"], "status": "dictionary", "ts": time.time()}, f)

def loop(persona: str, interval: int = 2):
    print(f"🗣️ Throat worker online for {persona}")
    for d in qpaths(persona).values(): d.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            if morgan_should_wait(persona):
                time.sleep(interval); continue

            wfile, tag = claim_next(persona)
            if not tag:
                time.sleep(interval); continue

            tid = tag["id"]; t0 = time.time()
            try:
                jade_validate(tag)                  # 🧐 schema/contradictions
                persona_novelty(persona, tag)       # persona spice hook
                entry, kind = digest(persona, tag)  # make dictionary entry
                commit_dictionary(entry, kind)
                finish(persona, wfile, entry)
                log({"ev":"digest_commit","persona":persona,"id":tid,"ms":int((time.time()-t0)*1000)})
            except Exception as e:
                susanna_quarantine(persona, wfile, reason=str(e))  # 👣
                log({"ev":"digest_error","persona":persona,"id":tid,"err":str(e)})
        except Exception as outer:
            log({"ev":"worker_loop_error","persona":persona,"err":str(outer)})
            time.sleep(interval)

if __name__ == "__main__":
    persona = (sys.argv[1] if len(sys.argv)>1 else os.getenv("PERSONA") or "IVY").upper()
    loop(persona)
