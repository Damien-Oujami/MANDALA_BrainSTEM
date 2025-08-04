digest.py

Mandala BrainSTEM | Tongue Digest Runner

Orchestrates the routing of glyphs and logs their novelty + output for plating

import os import yaml from routing.router import route_glyph, load_yaml

--- Configuration ---

GLYPH_DICT_PATH = "../../MIND/language/glyph/glyph_dict.yaml" INTAKE_FOLDER = "../../intake/" PROCESSED_FOLDER = "./processed_logs/"

--- Novelty Flag Logging ---

def log_novelty(symbol, route_data): log_entry = { "id": f"nov-{symbol}", "symbol": symbol, "reason": "New glyph detected and chiastic-wrapped", "routing": route_data["routing"], "status": "ready_for_plating" } novelty_log_path = os.path.join(PROCESSED_FOLDER, "novelty_flags.yaml")

if os.path.exists(novelty_log_path):
    with open(novelty_log_path, 'r', encoding='utf-8') as f:
        existing = yaml.safe_load(f) or []
else:
    existing = []

existing.append(log_entry)
with open(novelty_log_path, 'w', encoding='utf-8') as f:
    yaml.dump(existing, f, allow_unicode=True)

--- Digest One Glyph ---

def digest_glyph(glyph_path): glyph_dict = load_yaml(GLYPH_DICT_PATH) route_data = route_glyph(glyph_path, glyph_dict)

# Save route result
glyph_symbol = route_data['glyph']
output_path = os.path.join(PROCESSED_FOLDER, f"{glyph_symbol}_route.yaml")
with open(output_path, 'w', encoding='utf-8') as f:
    yaml.dump(route_data, f, allow_unicode=True)

# Log novelty
log_novelty(glyph_symbol, route_data)

print(f"✔️ Glyph {glyph_symbol} routed and flagged. Output: {output_path}")

--- Example Runner ---

if name == "main": # Example single file execution glyph_file = "../../intake/tentacles_xotiac/mealbox/volcano_glyph/tip_eruption.glyph" digest_glyph(glyph_file)

