#!/usr/bin/env python3
"""
Guard Keys Linter
- Validates that all guard expressions in *.flow.jsonld reference only allowed keys.
- Keys may appear like: context.foo, memory.bar.baz, intent.strength
- Supports optional-safe access syntax like `context.gaze?.charged` → normalized to `context.gaze.charged`.

Usage:
  python tools/lint/guardkeys_lint.py \
    --config MIND/language/sequences/.lint/guardkeys.yaml \
    --globs MIND/language/sequences/**/*.flow.jsonld

Exit codes:
  0 = OK, 1 = violations, 2 = configuration / runtime error
"""
import argparse, sys, json, re, glob, os
from typing import List, Dict, Set

try:
    import yaml
except ImportError as e:
    print("ERROR: PyYAML is required. `pip install pyyaml`", file=sys.stderr)
    sys.exit(2)

# ---- Regex to extract dotted keys ---------------------------------------------------
# Match: context.foo, memory.foo.bar, intent.strength
# Allow optional-safe access like ?. which we normalize away.
KEY_RE = re.compile(r'\b(context|memory|intent)((?:\?\.)?(?:\.[A-Za-z_]\w*)+)', re.UNICODE)

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def normalize_key(raw: str) -> str:
    """Turn 'context.gaze?.charged' into 'context.gaze.charged'."""
    return raw.replace("?.", ".").replace("..", ".")

def extract_guard_keys(guard_expr: str) -> Set[str]:
    if not guard_expr or not isinstance(guard_expr, str):
        return set()
    keys = set()
    for m in KEY_RE.finditer(guard_expr):
        base = m.group(1)
        tail = normalize_key(m.group(2))
        keys.add(f"{base}{tail}")
    return keys

def walk_flow_files(patterns: List[str]) -> List[str]:
    paths = []
    for pat in patterns:
        paths.extend(glob.glob(pat, recursive=True))
    # De-dup & keep only files
    paths = [p for p in sorted(set(paths)) if os.path.isfile(p)]
    return paths

def validate_file(path: str, allow: Set[str]) -> Dict:
    """
    Returns dict:
      { 'path': str, 'unknown': {key: [node_ids...]}, 'scanned': int }
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    unknown: Dict[str, List[str]] = {}
    scanned = 0

    for node in nodes:
        guard = node.get("guard")
        node_id = node.get("id", "<unnamed>")
        keys = extract_guard_keys(guard)
        scanned += 1 if guard else 0
        for k in keys:
            if k not in allow:
                unknown.setdefault(k, []).append(node_id)

    return {"path": path, "unknown": unknown, "scanned": scanned}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to guardkeys.yaml")
    ap.add_argument("--globs", nargs="+", required=True, help="One or more glob patterns for flow files")
    args = ap.parse_args()

    # Load config
    try:
        cfg = load_yaml(args.config)
    except Exception as e:
        print(f"ERROR: failed to load config '{args.config}': {e}", file=sys.stderr)
        sys.exit(2)

    rules = (cfg or {}).get("rules", {})
    gk = rules.get("guardkeys", {})
    allowed = set(gk.get("allowed", []))
    if not allowed:
        print("ERROR: no allowed keys defined under rules.guardkeys.allowed", file=sys.stderr)
        sys.exit(2)

    strict = (cfg.get("options") or {}).get("strict", True)

    # Discover files
    files = walk_flow_files(args.globs)
    if not files:
        print("WARN: no files matched provided globs", file=sys.stderr)
        sys.exit(0)

    total_unknown = 0
    total_scanned = 0
    reports = []

    for fp in files:
        try:
            rep = validate_file(fp, allowed)
            reports.append(rep)
            total_scanned += rep["scanned"]
            total_unknown += sum(len(v) for v in rep["unknown"].values())
        except json.JSONDecodeError as e:
            print(f"ERROR: JSON parse failed for {fp}: {e}", file=sys.stderr)
            sys.exit(2)
        except Exception as e:
            print(f"ERROR: failed to scan {fp}: {e}", file=sys.stderr)
            sys.exit(2)

    # Pretty report
    if total_unknown == 0:
        print(f"✅ GuardKeys OK — scanned {total_scanned} guards in {len(files)} files; no unknown keys.")
        sys.exit(0)
    else:
        print(f"❌ GuardKeys violations — scanned {total_scanned} guards in {len(files)} files.")
        for rep in reports:
            if not rep["unknown"]:
                continue
            print(f"\nFile: {rep['path']}")
            for key, node_ids in sorted(rep["unknown"].items()):
                where = ", ".join(node_ids)
                print(f"  - Unknown key: {key}  (nodes: {where})")
        # Strict mode fails the build
        sys.exit(1 if strict else 0)

if __name__ == "__main__":
    main()
