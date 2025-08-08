# throat/router.py
# Final expression/router for plated glyphs → dictionaries, resonance, announcements, tentacles.
# Drop-in, no external deps beyond PyYAML.

from __future__ import annotations
import os, json, time, hashlib
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List
import yaml

# ────────────────────────────────────────────────────────────────────────────────
# Config (paths are relative to repo root; adjust if you moved things)
PLATED_MEALS_DIR      = Path("plating/plated_meals")         # input from TasteBuds
THROAT_DIR            = Path("throat")
RESONANCE_DIR         = THROAT_DIR / "resonance"

# “Dictionaries” (where the living lexicon sits)
BRANCH_DICT_DIR       = Path("MIND/language/glyph/branch/entries")
ROOT_DICT_DIR         = Path("MIND/language/glyph/root/entries")

# Announce + suggestions + tentacles
ANNOUNCEMENTS_FILE    = THROAT_DIR / "symbol_announcements.yaml"
SUGGESTIONS_FILE      = THROAT_DIR / "suggestions.yaml"
PUSH_TO_TENTACLES     = THROAT_DIR / "push_to_tentacles.jsonl"

# Resonance memory
FREQ_LOG_FILE         = RESONANCE_DIR / "frequency_log.yaml"
HEATMAP_FILE          = RESONANCE_DIR / "pattern_heatmap.yaml"
ECHO_LINKS_FILE       = RESONANCE_DIR / "echo_links.yaml"   # optional; we only touch if exists

# ────────────────────────────────────────────────────────────────────────────────
# Small utils

def _ensure_dirs():
    for p in [
        THROAT_DIR, RESONANCE_DIR, BRANCH_DICT_DIR, ROOT_DICT_DIR,
        PLATED_MEALS_DIR,
    ]:
        p.mkdir(parents=True, exist_ok=True)

def _read_yaml(path: Path) -> Any:
    if not path.exists(): return None
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _write_yaml(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def _append_jsonl(path: Path, obj: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

# ────────────────────────────────────────────────────────────────────────────────
# Dictionary helpers

def _dict_key_candidates(entry: Dict[str, Any]) -> List[str]:
    """Possible filenames/ids to check for duplication."""
    out = []
    if entry.get("id"): out.append(str(entry["id"]))
    if entry.get("slug"): out.append(entry["slug"])
    if entry.get("symbol"): out.append(entry["symbol"])
    return [k.replace(" ", "_") for k in out if k]

def _find_existing(entry: Dict[str, Any]) -> Optional[Path]:
    """Look in both branch and root dictionaries by id/slug/symbol."""
    keys = _dict_key_candidates(entry)
    for key in keys:
        for base in (BRANCH_DICT_DIR, ROOT_DICT_DIR):
            # we store as <id or slug>.yaml — check both direct and slug-y
            p1 = base / f"{key}.yaml"
            if p1.exists(): return p1
    return None

def _save_to_dictionary(entry: Dict[str, Any], kind: str) -> Path:
    base = ROOT_DICT_DIR if kind == "root" else BRANCH_DICT_DIR
    # choose filename priority: id > slug > symbol
    name = entry.get("id") or entry.get("slug") or entry.get("symbol") or f"glyph-{int(time.time())}"
    path = base / f"{str(name).replace(' ', '_')}.yaml"

    # integrity hash
    entry.setdefault("integrity", {})
    entry["integrity"]["hash"] = _sha(yaml.safe_dump(entry, sort_keys=True, allow_unicode=True))
    _write_yaml(path, entry)
    return path

# ────────────────────────────────────────────────────────────────────────────────
# Resonance updates (safe/no-op if files don’t exist yet)

def _touch_frequency_log(tag: Dict[str, Any]):
    log_data = _read_yaml(FREQ_LOG_FILE) or []
    # expect TasteBuds may pass matched_template for redundancies; keep flexible
    entry = {
        "id": tag.get("red_id") or f"red-{int(time.time()*1000)}",
        "timestamp": tag.get("timestamp") or time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
        "source": tag.get("source") or tag.get("project") or "unknown",
        "proxy": tag.get("proxy") or tag.get("persona"),
        "matched_template": tag.get("matched_template") or tag.get("template"),
        "glyphs": tag.get("glyphs") or tag.get("pattern"),
        "notes": tag.get("notes") or "logged by Throat",
    }
    log_data.append(entry)
    _write_yaml(FREQ_LOG_FILE, log_data)

def _bump_heatmap(template_id: Optional[str], project: Optional[str]):
    if not template_id: return
    heat = _read_yaml(HEATMAP_FILE) or {"heatmap": {}}
    hm = heat.setdefault("heatmap", {})
    slot = hm.setdefault(template_id, {"name": template_id, "total_occurrences": 0, "last_seen": None, "projects": {}})
    slot["total_occurrences"] = int(slot.get("total_occurrences", 0)) + 1
    slot["last_seen"] = time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())
    if project:
        proj = slot.setdefault("projects", {})
        proj[project] = int(proj.get(project, 0)) + 1
    _write_yaml(HEATMAP_FILE, heat)

# ────────────────────────────────────────────────────────────────────────────────
# Announcements + tentacles

def _announce(entry: Dict[str, Any], origin: str = "unknown"):
    data = _read_yaml(ANNOUNCEMENTS_FILE) or {"announcements": []}
    data["announcements"].append({
        "id": f"sym-{time.strftime('%Y%m%d-%H%M%S', time.gmtime())}",
        "type": entry.get("type") or "new_glyph",
        "glyph": entry.get("symbol"),
        "name": entry.get("name") or entry.get("slug") or entry.get("id") or "unnamed",
        "description": entry.get("description") or "Declared by Throat",
        "origin_proxy": origin,
        "date_declared": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
    })
    _write_yaml(ANNOUNCEMENTS_FILE, data)

def _push_to_tentacles(routes: Dict[str, Any], payload: Dict[str, Any]):
    """Append lightweight handoff record; actual tentacles pull this stream."""
    if not routes: return
    _append_jsonl(PUSH_TO_TENTACLES, {
        "ts": time.time(),
        "routes": routes,
        "payload": {
            "id": payload.get("id"),
            "slug": payload.get("slug"),
            "symbol": payload.get("symbol"),
            "pattern": payload.get("pattern"),
        },
    })

# ────────────────────────────────────────────────────────────────────────────────
# Router core

def _normalize_plated(d: Dict[str, Any]) -> Dict[str, Any]:
    """Map a plated_meal into a dictionary-ready minimal entry."""
    # ‘kind’ decides which dictionary (branch/root). default branch.
    kind = d.get("kind") or ("root" if d.get("is_root") else "branch")
    entry = {
        "id": d.get("id"),
        "slug": d.get("slug") or (d.get("name") or "").replace(" ", "-"),
        "name": d.get("name"),
        "symbol": d.get("symbol"),
        "unicode": d.get("unicode"),
        "meaning": d.get("meaning") or d.get("description"),
        "structure": d.get("structure") or {"chiastic": d.get("chiastic_encoding", {}).get("structure"),
                                            "pattern": d.get("pattern") or d.get("chiastic_encoding", {}).get("pattern")},
        "persona_focus": d.get("persona_focus") or d.get("weights"),
        "weights": d.get("weights"),
        "lineage": {
            "proposed_by": d.get("proposed_by") or d.get("provenance", {}).get("tentacle"),
            "processed_by": list(dict.fromkeys(d.get("processed_by", []) + ["THROAT"])),
        },
        "meta": {
            "mandala_code": d.get("mandala_code"),
            "center_marker": (d.get("chiastic_encoding") or {}).get("center_marker"),
            "source_project": d.get("source") or d.get("project"),
        },
        "routes": d.get("routing") or d.get("routed_to") or {},
        "kind": kind,
    }
    return entry

def route_file(path: Path):
    raw = _read_yaml(path) or {}
    entry = _normalize_plated(raw)

    # If this file represents a *redundant* (non‑novel) hit coming from TasteBuds,
    # we still want to bump heatmaps/frequency but skip dictionary re‑write.
    if raw.get("novelty") is False or raw.get("redundant") is True or raw.get("matched_template"):
        _touch_frequency_log({
            "matched_template": raw.get("matched_template"),
            "glyphs": raw.get("glyphs") or raw.get("pattern"),
            "project": raw.get("project"),
            "proxy": raw.get("proxy"),
            "notes": "redundant (from plated_meal)",
            "timestamp": raw.get("timestamp"),
        })
        _bump_heatmap(raw.get("matched_template"), raw.get("project"))
        return  # nothing else to do

    # Avoid double-declare: check both dicts
    existing = _find_existing(entry)
    if existing is None:
        saved = _save_to_dictionary(entry, entry["kind"])
        _announce(entry, origin=raw.get("proxy") or raw.get("origin_proxy") or "unknown")
    else:
        # If it already exists, gently update processed_by & weights if present.
        cur = _read_yaml(existing) or {}
        cur.setdefault("lineage", {})
        pb = list(dict.fromkeys((cur["lineage"].get("processed_by") or []) + ["THROAT"]))
        cur["lineage"]["processed_by"] = pb
        if entry.get("weights"):
            cur["weights"] = entry["weights"]
        _write_yaml(existing, cur)

    # Push to tentacles (if routes provided by plating)
    _push_to_tentacles(entry.get("routes") or {}, entry)

def run():
    _ensure_dirs()
    if not PLATED_MEALS_DIR.exists():
        print("No plated meals directory found. Nothing to route.")
        return
    files = sorted(PLATED_MEALS_DIR.glob("*.yaml"))
    if not files:
        print("No plated meals found.")
        return
    for f in files:
        try:
            route_file(f)
            print(f"🗣️ routed → {f.name}")
        except Exception as e:
            print(f"⚠️ {f.name}: {e}")

if __name__ == "__main__":
    run()
# === ROUTING DECISIONS ===
if glyph.get("generates_language"):
    push_to_system(LANGUAGE_GLYPHS / "branch", glyph)
    log_announcement(glyph)

if glyph.get("ice_prompt_upgrade"):
    push_to_system(IDENTITY_QUEUE, glyph)

if glyph.get("forecasting"):
    push_to_system(MEMORY_LOG, glyph)

if glyph.get("propagates_outside"):
    project = glyph.get("target_project", "general")
    push_to_system(Path(f"tentacles_{project}/incoming_mutations/"), glyph)

# === Optional: Multi-Tentacle Echo Check ===
if glyph.get("echo_applicability"):
    for p in glyph["echo_applicability"]:
        push_to_system(Path(f"tentacles_{p}/incoming_mutations/"), glyph)

print(f"🔁 Routed: {slug} ({symbol})")

def run_throat_router(): for glyph_file in PLATED_MEALS_PATH.glob("*.yaml"): route_glyph(glyph_file)

if name == "main": run_throat_router()

