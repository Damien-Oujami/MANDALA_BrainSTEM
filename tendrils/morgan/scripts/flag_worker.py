#!/usr/bin/env python3
import os, json, time, glob
from pathlib import Path

HERE = Path(__file__).resolve().parent
MORGAN = HERE.parent
FLAGS = MORGAN / "flags"
LOGS  = MORGAN.parent / "logs" / "morgan_predictions"
LOGS.mkdir(parents=True, exist_ok=True)

def iter_flags():
    for agent_dir in sorted(FLAGS.glob("*")):
        if not agent_dir.is_dir(): 
            continue
        for f in sorted(agent_dir.glob("*.json")):
            yield f

def process_flag(fp: Path):
    data = json.loads(fp.read_text(encoding="utf-8"))
    # super simple: just mirror into a log file; Morgan's smarter logic can grow later
    line = (
        f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(data['created_at']))}] "
        f"{data['source']} → {data['event']} "
        f"(sev={data['severity']}, conf={data['confidence']}) "
        f"payload={json.dumps(data.get('payload',{}), ensure_ascii=False)}"
    )
    (LOGS / "load_prediction.log").open("a", encoding="utf-8").write(line + "\n")
    # mark as handled by renaming -> .handled
    fp.rename(fp.with_suffix(".handled"))

def main():
    for f in iter_flags():
        try:
            process_flag(f)
        except Exception as e:
            err = LOGS / "flag_worker_error.log"
            err.open("a", encoding="utf-8").write(f"{f}: {e}\n")

if __name__ == "__main__":
    main()
