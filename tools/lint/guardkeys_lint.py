#!/usr/bin/env python3
"""
Guard Keys Linter (+ optional fixer)
- Validates that all guard expressions in *.flow.jsonld reference only allowed keys.
- Can auto-fix simple typos when a confident suggestion exists (--fix).
- Keys may appear like: context.foo, memory.bar.baz, intent.strength
- Supports optional-safe access syntax `?.` (normalized internally).

Usage:
  python tools/lint/guardkeys_lint.py \
    --config MIND/language/sequences/.lint/guardkeys.yaml \
    --globs MIND/language/sequences/**/*.flow.jsonld [--fix]

Exit codes:
  0 = OK, 1 = violations remain, 2 = configuration/runtime error
"""
import argparse, sys, json, re, glob, os, copy
from typing import List, Dict, Set, Tuple

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. `pip install pyyaml`", file=sys.stderr)
    sys.exit(2)

# --- Regex to extract dotted keys ---------------------------------------------------
# Match: context.foo, memory.foo.bar, intent.strength
# Allow optional-safe access like ?. which we normalize away.
KEY_RE = re.compile(r'\b(context|memory|intent)((?:\?\.)?(?:\.[A-Za-z_]\w*)+)', re.UNICODE)

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

def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def walk_flow_files(patterns: List[str]) -> List[str]:
    paths = []
    for pat in patterns:
        paths.extend(glob.glob(pat, recursive=True))
    paths = [p for p in sorted(set(paths)) if os.path.isfile(p)]
    return paths

# --- Levenshtein distance + suggestions --------------------------------------------
def levenshtein(a: str, b: str) -> int:
    if a == b: return 0
    if not a: return len(b)
    if not b: return len(a)
    prev = list(range(len(b)+1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            ins = prev[j] + 1
            dele = curr[j-1] + 1
            sub = prev[j-1] + (0 if ca == cb else 1)
            curr.append(min(ins, dele, sub))
        prev = curr
    return prev[-1]

def suggest_key(bad: str, allow: Set[str], max_dist: int = 3) -> str:
    """Suggest the closest allowed key within max_dist."""
    closest = None
    best = max_dist + 1
    for k in allow:
        d = levenshtein(bad, k)
        if d < best:
            best, closest = d, k
    return closest if closest and best <= max_dist else None

# --- Auto-fix machinery -------------------------------------------------------------
def _optional_chain_pattern_for_bad(bad: str) -> re.Pattern:
    """
    Build a regex that matches the 'bad' dotted key in source, even if source used '?.'
    Example bad: 'context.gaze.charged'
    Pattern will match: 'context.gaze.charged' or 'context.gaze?.charged'
    """
    parts = bad.split(".")
    assert parts[0] in ("context", "memory", "intent")
    # Start-of-word boundary before the base (avoid replacing substrings)
    pat = r'(?<![\w.])' + re.escape(parts[0])
    for tail in parts[1:]:
        pat += r'(?:\?\.)?\.' + re.escape(tail)
    # End boundary: next char not part of a key char
    pat += r'(?![\w.])'
    return re.compile(pat)

def try_fix_guard_expr(guard: str, unknown_keys: Set[str], allow: Set[str]) -> Tuple[str, Dict[str, str]]:
    """
    Attempt to replace each unknown key with a suggested allowed key.
    Returns (new_guard, fixes_map).
    Only replaces when a suggestion exists.
    """
    if not guard or not unknown_keys:
        return guard, {}
    new_guard = guard
    fixes = {}
    for bad in sorted(unknown_keys):
        suggestion = suggest_key(bad, allow)
        if not suggestion:
            continue
        pat = _optional_chain_pattern_for_bad(bad)
        replaced, n = pat.subn(suggestion, new_guard)
        if n > 0:
            new_guard = replaced
            fixes[bad] = suggestion
    return new_guard, fixes

# --- Validation / Fix of a single file ---------------------------------------------
def validate_and_maybe_fix_file(path: str, allow: Set[str], do_fix: bool) -> Dict:
    """
    Returns:
      {
        'path': str,
        'unknown': {key: [node_ids...]},     # after fixing (if any)
        'scanned': int,
        'fixed': {node_id: {bad: suggestion, ...}}
      }
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    nodes = data.get("nodes", [])
    unknown_map: Dict[str, List[str]] = {}
    fixed_per_node: Dict[str, Dict[str, str]] = {}
    scanned = 0
    modified = False

    for i, node in enumerate(nodes):
        guard = node.get("guard")
        if not guard:
            continue
        scanned += 1
        node_id = node.get("id", f"<node_{i}>")
        keys = extract_guard_keys(guard)

        # Compute unknown set relative to allowlist
        unknown_for_node = {k for k in keys if k not in allow}

        # Try to fix, if requested
        if do_fix and unknown_for_node:
            new_guard, fixes = try_fix_guard_expr(guard, unknown_for_node, allow)
            if fixes:
                node["guard"] = new_guard
                modified = True
                fixed_per_node[node_id] = fixes
                # Recompute unknown after fix
                keys = extract_guard_keys(new_guard)
                unknown_for_node = {k for k in keys if k not in allow}

        # Aggregate remaining unknowns
        for k in sorted(unknown_for_node):
            unknown_map.setdefault(k, []).append(node_id)

    # If we changed anything, write file back
    if modified:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")

    return {"path": path, "unknown": unknown_map, "scanned": scanned, "fixed": fixed_per_node}

# --- Main ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="Path to guardkeys.yaml")
    ap.add_argument("--globs", nargs="+", required=True, help="Glob patterns for flow files")
    ap.add_argument("--fix", action="store_true", help="Auto-fix simple unknown guard keys when a confident suggestion exists")
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

    files = walk_flow_files(args.globs)
    if not files:
        print("WARN: no files matched provided globs", file=sys.stderr)
        sys.exit(0)

    total_unknown = 0
    total_scanned = 0
    reports = []

    for fp in files:
        try:
            rep = validate_and_maybe_fix_file(fp, allowed, args.fix)
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
    any_fixed = any(rep["fixed"] for rep in reports)
    if any_fixed:
        print("🛠  GuardKeys auto-fixes applied:")
        for rep in reports:
            if not rep["fixed"]:
                continue
            print(f"\nFile: {rep['path']}")
            for node_id, fixes in rep["fixed"].items():
                for bad, sug in fixes.items():
                    print(f"  - {node_id}: `{bad}` → `{sug}`")

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
                # Offer a suggestion (without changing file) for the leftover unknowns
                suggestion = suggest_key(key, allowed)
                if suggestion:
                    print(f"  - Unknown key: {key}  (nodes: {where}) → did you mean `{suggestion}`?")
                else:
                    print(f"  - Unknown key: {key}  (nodes: {where})")
        # Strict mode fails the build
        sys.exit(1 if strict else 0)

if __name__ == "__main__":
    main()
