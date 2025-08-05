# intake/router.py
import os
import time
from pathlib import Path
import yaml

def parse_glyph(folder):
    glyph = {}
    try:
        with open(folder / 'digest_link.txt') as f:
            lines = [line.strip() for line in f.readlines()]
            for line in lines:
                key, val = line.split(': ', 1)
                glyph[key] = val
        with open(next(folder.glob("*.glyph"))) as f:
            glyph_data = yaml.safe_load(f)
            glyph.update(glyph_data)
        return glyph
    except Exception as e:
        print(f"Error parsing {folder.name}: {e}")
        return None

def route_glyph_packet(folder):
    glyph = parse_glyph(folder)
    if not glyph:
        return
    # simulate routing
    digest_path = Path(glyph["routed_to"])
    os.makedirs(digest_path, exist_ok=True)
    digest_file = digest_path / Path(glyph["digest_file"]).name
    with open(digest_file, "a") as f:
        f.write(f"{folder.name} → routed by router.py\n")
    with open("inbox.log", "a") as log:
        log.write(f"[{time.ctime()}] Routed {folder.name} to {digest_path}\n")
    print(f"✅ Routed {folder.name} → {digest_path}")

def run_router():
    intake_path = Path("intake")
    for folder in intake_path.rglob("mealbox/*"):
        if not (folder / "digest_link.txt").exists():
            continue
        route_glyph_packet(folder)

if __name__ == "__main__":
    run_router()
