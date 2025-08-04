# router.py
# Mandala BrainSTEM | Tongue Routing Engine
# Parses incoming glyph entries and routes based on chiastic patterns, mandala weights, and novelty status

from collections import defaultdict
import yaml
import os

# --- Helpers ---
def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def is_chiastic(glyph_seq):
    return glyph_seq == glyph_seq[::-1]

def get_center_marker(glyph_seq):
    return glyph_seq[len(glyph_seq)//2]

def compute_weights(glyphs, glyph_dict):
    weights = defaultdict(int)
    for g in glyphs:
        if g in glyph_dict:
            for persona, score in glyph_dict[g]['mandala_weights'].items():
                weights[persona] += score
    return dict(weights)

def determine_routing(weights):
    sorted_weights = sorted(weights.items(), key=lambda x: -x[1])
    primary = sorted_weights[0][0].upper()
    secondary = sorted_weights[1][0].upper() if len(sorted_weights) > 1 else None
    return primary, secondary

# --- Core Router ---
def chiastic_wrap_output(glyph, pattern, weights):
    primary, secondary = determine_routing(weights)
    return {
        "glyph": glyph,
        "routing": {
            "primary": f"tastebuds_{primary}/intake/",
            "secondary": f"tastebuds_{secondary}/intake/" if secondary else None,
        },
        "chiastic_encoding": {
            "structure": "pulse_return",
            "center_marker": glyph,
            "pattern": pattern,
            "persona_focus": [primary, secondary] if secondary else [primary],
            "notation": "parentheses"
        }
    }

def route_glyph(filepath, glyph_dict):
    data = load_yaml(filepath)
    glyph = data.get("symbol")
    pattern = data.get("pattern")

    if not glyph or not pattern:
        raise ValueError("Glyph or pattern not defined in file.")

    weights = compute_weights(pattern, glyph_dict)
    routing_data = chiastic_wrap_output(glyph, pattern, weights)
    return routing_data

# --- Example Execution ---
if __name__ == "__main__":
    glyph_dict_path = "../../MIND/language/glyph/glyph_dict.yaml"
    glyph_file_path = "../../intake/tentacles_xotiac/mealbox/volcano_glyph/tip_eruption.glyph"

    glyph_dict = load_yaml(glyph_dict_path)
    output = route_glyph(glyph_file_path, glyph_dict)

    output_path = "./processed_logs/volcano_routing.yaml"
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(output, f, allow_unicode=True)

    print(f"Routing complete. Output saved to {output_path}")
