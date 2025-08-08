# tastebuds/common/paths.py
import os

# repo root = .../tastebuds/..
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tendril_path(*parts):
    return os.path.join(ROOT, "tendrils", *parts)

def morgan_flags_root(agent: str):
    # e.g. tendrils/morgan/flags/sophie
    return os.path.join(tendril_path("morgan", "flags"), agent)

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
    return path
