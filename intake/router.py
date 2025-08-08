# intake/router.py
import os, time, yaml, json, hashlib, shutil
from pathlib import Path

INTAKE = Path("intake")
QUAR   = INTAKE / "_quarantine"
LOG    = INTAKE / "inbox.log"
QUAR.mkdir(parents=True, exist_ok=True)

REQ_KEYS = {"id","name","routing","persona_focus","mandala_weights"}

def sha256_text(text:str)->str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_packet(folder: Path):
    # prefer packet.yaml, else first *.glyph
    cand = (folder / "packet.yaml")
    if not cand.exists():
        g = list(folder.glob("*.glyph"))
        if not g: 
            raise ValueError("No packet file found")
        cand = g[0]
    data = yaml.safe_load(cand.read_text(encoding="utf-8"))
    missing = REQ_KEYS - data.keys()
    if missing:
        raise ValueError(f"Missing keys: {sorted(missing)}")
    return data, cand

def quarantine(folder: Path, reason: str):
    dest = QUAR / f"{folder.name}__{int(time.time())}"
    shutil.move(str(folder), str(dest))
    with LOG.open("a", encoding="utf-8") as log:
        log.write(f"[{time.ctime()}] QUARANTINE {dest.name} :: {reason}\n")

def route(folder: Path):
    try:
        data, src = load_packet(folder)
        rid = data["routing"].get("primary")
        if not rid:
            # fallback to persona_focus[0]
            pf = data.get("persona_focus", [])
            if not pf:
                raise ValueError("No routing.primary or persona_focus")
            rid = f"tastebuds_{pf[0].upper()}/intake/"
        digest_path = Path(rid)
        digest_path.mkdir(parents=True, exist_ok=True)

        # atomic “done” marker
        done = folder / ".done"
        done.write_text("ok", encoding="utf-8")

        # append delivery receipt (append-only)
        receipt = digest_path / f"{data['id']}.receipt"
        with receipt.open("a", encoding="utf-8") as r:
            r.write(json.dumps({
                "ts": time.time(),
                "glyph_id": data["id"],
                "from": str(folder),
                "to": str(digest_path),
                "hash": sha256_text(src.read_text(encoding="utf-8"))
            }) + "\n")

        with LOG.open("a", encoding="utf-8") as log:
            log.write(f"[{time.ctime()}] ROUTED {data['id']} -> {digest_path}\n")

        # optional: move folder to archive
        shutil.move(str(folder), str(folder.parent / f"_{folder.name}"))

    except Exception as e:
        quarantine(folder, str(e))

def run_router():
    for folder in INTAKE.rglob("mealbox/*"):
        if not folder.is_dir(): 
            continue
        if (folder / ".done").exists():
            continue
        route(folder)

if __name__ == "__main__":
    while True:
        run_router()
        time.sleep(5)
