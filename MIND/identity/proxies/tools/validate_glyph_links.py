#!/usr/bin/env python3
import json, sys, glob, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", ".."))  # up to Mind/
GLYPH_FILES = [
    os.path.join(ROOT, "language/glyph/root/root_glyphs.json"),
    os.path.join(ROOT, "language/glyph/branch/branch_glyphs.json"),
]
ABB_GLOBS = [
    os.path.join(ROOT, "Identity/Proxies/ABB_Libraries/**/*@*.yml"),
    os.path.join(ROOT, "Identity/Proxies/ABB_Libraries/**/*@*.yaml"),
]

def load_glyph_names():
    names = set()
    for path in GLYPH_FILES:
        if not os.path.exists(path): 
            continue
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"[ERROR] {path}: {e}")
                continue
            for g in data:
                n = g.get("name") or ""
                # also allow "emoji name" forms like "🌊 Waveprint"
                emoji = g.get("emoji") or ""
                if n: names.add(n)
                if emoji and n: names.add(f"{emoji} {n}")
    return names

def scan_abbs(names):
    missing = []
    for path in [p for g in ABB_GLOBS for p in glob.glob(g, recursive=True)]:
        try:
            txt = open(path, "r", encoding="utf-8").read()
        except Exception:
            continue
        # crude: extract under 'glyphs:\n  triggers: [...]'
        m = re.search(r"glyphs:\s*[\s\S]*?triggers:\s*\[([^\]]*)\]", txt, re.M)
        if not m: 
            continue
        items = [s.strip().strip('"\'') for s in m.group(1).split(",") if s.strip()]
        for it in items:
            if it not in names:
                missing.append((os.path.relpath(path, ROOT), it))
    return missing

if __name__ == "__main__":
    names = load_glyph_names()
    missing = scan_abbs(names)
    if not missing:
        print("OK: all ABB glyph triggers exist in glyph JSONs.")
        sys.exit(0)
    print("Missing glyph references:")
    for path, it in missing:
        print(f" - {path}: {it}")
    sys.exit(1)
