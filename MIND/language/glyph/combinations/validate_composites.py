#!/usr/bin/env python3
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
def load_json(path):
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

root_glyphs = load_json(os.path.join(ROOT, "root", "root_glyphs.json"))
branch_glyphs = load_json(os.path.join(ROOT, "branch", "branch_glyphs.json"))
composites = load_json(os.path.join(ROOT, "combinations", "composite_glyphs.json"))

# Build a set of acceptable canonical names (with and without emoji prefix)
canon = set()
for entry in root_glyphs + branch_glyphs:
    n = entry.get("name","")
    e = entry.get("emoji","")
    if n: canon.add(n)
    if e and n and not n.startswith(e):
        canon.add(f"{e} {n}")

ok = True

# 1) composite names must not contain emoji
emoji_re = re.compile(r"[\U0001F300-\U0001FAFF]")
for c in composites:
    if emoji_re.search(c.get("name","")):
        print(f"[ERROR] Composite name contains emoji: {c['name']}")
        ok = False

# 2) each composed_of entry must be a known canonical glyph name (with or without emoji prefix)
for c in composites:
    for ref in c.get("composed_of", []):
        if ref not in canon:
            print(f"[ERROR] Unknown canonical glyph reference in '{c['name']}': {ref}")
            ok = False

if ok:
    print("OK: composite names are emoji-free and references resolve to canonical glyphs.")
    sys.exit(0)
sys.exit(1)
