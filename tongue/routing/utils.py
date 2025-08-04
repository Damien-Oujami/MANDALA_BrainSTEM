utils.py

Optional Advanced Helpers for Tongue Digest System

Used by both router and digest for future automation, error handling, and recursion safety

import os import yaml from datetime import datetime

--- YAML IO Utilities ---

def load_yaml(path): with open(path, 'r', encoding='utf-8') as f: return yaml.safe_load(f)

def save_yaml(data, path): with open(path, 'w', encoding='utf-8') as f: yaml.dump(data, f, allow_unicode=True)

--- Timestamp Utility ---

def get_timestamp(): return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

--- Path Tools ---

def ensure_dir(path): if not os.path.exists(path): os.makedirs(path)

--- Digest Log Entry Creator ---

def create_digest_log(symbol, routing_data): return { "id": f"nov-{symbol}", "symbol": symbol, "reason": "New glyph detected", "routing": routing_data.get("routing", {}), "status": "ready_for_plating", "timestamp": get_timestamp() }

--- Chiastic Check ---

def is_chiastic_pattern(seq): return seq == seq[::-1] and len(seq) % 2 == 1

--- Safe Append to YAML Array ---

def append_to_yaml_log(entry, path): if os.path.exists(path): with open(path, 'r', encoding='utf-8') as f: existing = yaml.safe_load(f) or [] else: existing = [] existing.append(entry) save_yaml(existing, path)

