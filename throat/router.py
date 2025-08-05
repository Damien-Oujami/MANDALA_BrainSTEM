import os import yaml from pathlib import Path from datetime import datetime

=== CONFIG ===

PLATED_MEALS_PATH = Path("plating/plated_meals") SYMBOL_ANNOUNCEMENTS = Path("throat/symbol_announcements.yaml") SUGGESTIONS_LOG = Path("throat/suggestions.yaml") PUSH_TO_TENTACLES = Path("throat/push_to_tentacles.json") IDENTITY_QUEUE = Path("Mind/Identity/ICE_queue/") LANGUAGE_GLYPHS = Path("Mind/Language/glyph/") MEMORY_LOG = Path("Mind/Memory/pattern_log/")

=== UTILS ===

def load_yaml(file): with open(file) as f: return yaml.safe_load(f)

def write_yaml(file, data): with open(file, 'w') as f: yaml.dump(data, f)

def log_announcement(glyph_data): if not SYMBOL_ANNOUNCEMENTS.exists(): announcements = {"announcements": []} else: announcements = load_yaml(SYMBOL_ANNOUNCEMENTS)

entry = {
    "id": f"sym-{datetime.utcnow().strftime('%Y-%m-%d-%H%M')}",
    "type": "new_glyph",
    "glyph": glyph_data.get("symbol", "?"),
    "name": glyph_data.get("name", glyph_data.get("slug", "unnamed")),
    "description": glyph_data.get("description", "Auto-declared by Throat"),
    "origin_proxy": glyph_data.get("origin", "unknown"),
    "date_declared": datetime.utcnow().isoformat()
}
announcements["announcements"].append(entry)
write_yaml(SYMBOL_ANNOUNCEMENTS, announcements)

def push_to_system(target, glyph_data): # Write to proper target folder or JSON os.makedirs(target, exist_ok=True) file = Path(target) / f"{glyph_data['slug']}.yaml" with open(file, 'w') as f: yaml.dump(glyph_data, f)

def route_glyph(glyph_file): with open(glyph_file) as f: glyph = yaml.safe_load(f)

destination = glyph.get("routed_to")
symbol = glyph.get("symbol")
slug = glyph.get("slug", "unnamed")

# === FINAL REDUNDANCY CHECK ===
# Placeholder: Could compare to `pattern_heatmap.yaml`

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

