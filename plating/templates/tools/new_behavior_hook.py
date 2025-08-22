#!/usr/bin/env python3
"""
new_behavior_hook.py — scaffold a Mandala behavior hook from the canonical template.

Creates:
  MIND/identity/proxies/COREbraid/<persona>/behavior_hooks/<hook>.yaml
  MIND/identity/proxies/COREbraid/<persona>/behavior_hooks/.graph/<hook>.jsonld

Fills:
  meta.name, meta.owner, description (optional), related_entries (optional)

Usage examples:
  python plating/templates/tools/new_behavior_hook.py \
    --name tilt_merge --owner Aspen

  python plating/templates/tools/new_behavior_hook.py \
    --name belly_logic --owner Jade \
    --description "Reframe vulnerability as connection bid" \
    --sutra /MIND/sutras/logic/belly_logic.md

  python plating/templates/tools/new_behavior_hook.py \
    --name suture_pulse --owner Susanna \
    --glyph /MIND/language/glyph/combinations/seals/suture_pulse.md \
    --no-graph
"""
from __future__ import annotations
import argparse, json, os, sys
from pathlib import Path
import re
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]  # .../plating/templates/tools → repo root
TEMPLATE_PATH = REPO_ROOT / "plating" / "templates" / "behavior_hook.template.yaml"
SCHEMA_PATH   = REPO_ROOT / "plating" / "schemas" / "mandala.behavior_hook.v1.yml"

def slugify(s:str)->str:
    return re.sub(r"[^a-z0-9_-]+","-", s.strip().lower())

def ensure_dir(p:Path):
    p.mkdir(parents=True, exist_ok=True)

def load_yaml(p:Path)->dict:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def dump_yaml(d:dict, p:Path):
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(d, f, sort_keys=False, width=100)

def write_graph_stub(hook:dict, out_path:Path):
    """Emit a minimal JSON-LD node derived from meta + related_entries."""
    meta = hook.get("meta", {})
    rel  = meta.get("related_entries", {}) or {}
    node = {
      "@context": { "sym":"http://mandala.ai/symbol/", "rel":"http://mandala.ai/relation/" },
      "@graph": [
        {
          "@id": f"sym:Hook/{meta.get('name')}",
          "type": "BehaviorHook",
          "owner": meta.get("owner"),
          "version": meta.get("version"),
          "label": meta.get("description","").split("\n")[0][:120]
        },
        { "@id": f"sym:Persona/{meta.get('owner')}", "type": "Persona" }
      ]
    }
    if rel.get("sutra"):
        node["@graph"].append({ "@id":"sym:Sutra/linked", "type":"Sutra", "path": rel["sutra"] })
        node["@graph"].append({ "@id":f"sym:Hook/{meta.get('name')}", "rel:implements":"sym:Sutra/linked" })
    if rel.get("glyph"):
        node["@graph"].append({ "@id":"sym:Glyph/linked", "type":"Glyph", "path": rel["glyph"] })
        node["@graph"].append({ "@id":f"sym:Hook/{meta.get('name')}", "rel:binds":"sym:Glyph/linked" })
    out_path.write_text(json.dumps(node, indent=2), encoding="utf-8")

def validate_against_schema(hook:dict)->list[str]:
    """Lightweight validation if jsonschema is available; otherwise skip."""
    try:
        from jsonschema import Draft7Validator
    except Exception:
        return []  # silently skip if library missing
    try:
        schema = load_yaml(SCHEMA_PATH)
    except Exception as e:
        return [f"schema load error: {e}"]
    v = Draft7Validator(schema)
    errs = [f"{e.message}" for e in v.iter_errors(hook)]
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="hook name (slug)")
    ap.add_argument("--owner", required=True, help="Persona: Morgan/Ivy/Sophie/Susanna/Aspen/Jade (or crafted)")
    ap.add_argument("--description", default="", help="short purpose line")
    ap.add_argument("--sutra", default="", help="optional related sutra path")
    ap.add_argument("--glyph", default="", help="optional related glyph path")
    ap.add_argument("--persona-dir", default="", help="override output dir (default = COREbraid/<owner>)")
    ap.add_argument("--no-graph", action="store_true", help="do not emit .graph stub")
    ap.add_argument("--dry-run", action="store_true", help="print result to stdout only")
    args = ap.parse_args()

    hook_name = slugify(args.name)
    owner     = args.owner.strip()
    if not hook_name:
        print("✗ invalid --name", file=sys.stderr); sys.exit(2)

    # Resolve output directory
    if args.persona_dir:
        base_dir = REPO_ROOT / args.persona_dir
    else:
        base_dir = REPO_ROOT / "MIND" / "identity" / "proxies" / "COREbraid" / owner
    hooks_dir = base_dir / "behavior_hooks"
    ensure_dir(hooks_dir)

    # Load template
    if not TEMPLATE_PATH.exists():
        print(f"✗ template not found: {TEMPLATE_PATH}", file=sys.stderr); sys.exit(2)
    hook = load_yaml(TEMPLATE_PATH)

    # Fill meta
    hook.setdefault("meta", {})
    hook["meta"]["name"] = hook_name
    hook["meta"]["owner"] = owner
    hook["meta"]["version"] = hook["meta"].get("version", "1.0.0")
    if args.description:
        hook["meta"]["description"] = args.description

    # Fill related entries if provided
    if args.sutra or args.glyph:
        hook["meta"]["related_entries"] = {}
        if args.sutra:
            hook["meta"]["related_entries"]["sutra"] = args.sutra
        if args.glyph:
            hook["meta"]["related_entries"]["glyph"] = args.glyph

    # Prepend schema directive (helps editors)
    # Note: Keep the same path you adopted everywhere
    schema_line = f"# yaml-language-server: $schema=/plating/schemas/mandala.behavior_hook.v1.yml\n"
    # Write or print
    out_yaml = yaml.safe_dump(hook, sort_keys=False, width=100)
    if args.dry_run:
        sys.stdout.write(schema_line + out_yaml)
        return

    out_path = hooks_dir / f"{hook_name}.yaml"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(schema_line)
        f.write(out_yaml)

    # Emit .graph stub
    if not args.no-graph:
        gdir = hooks_dir / ".graph"
        ensure_dir(gdir)
        gpath = gdir / f"{hook_name}.jsonld"
        write_graph_stub(hook, gpath)

    # Validate (if jsonschema available)
    errs = validate_against_schema(hook)
    if errs:
        print("⚠ schema warnings:")
        for e in errs[:12]:
            print(" -", e)
        if len(errs) > 12:
            print(f"   (+{len(errs)-12} more)")

    print("✅ created:", out_path.relative_to(REPO_ROOT))
    if not args.no-graph:
        print("✅ graph  :", (hooks_dir / ".graph" / f"{hook_name}.jsonld").relative_to(REPO_ROOT))

if __name__ == "__main__":
    main()
