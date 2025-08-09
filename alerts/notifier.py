# alerts/notifier.py
# Tails alerts/events.jsonl and POSTs each event to your n8n webhook (which forwards to Telegram).

import os, time, json
import requests

WEBHOOK = os.getenv("N8N_WEBHOOK")  # e.g. https://n8n.example/webhook/brainstem
BUS = "alerts/events.jsonl"

def tail(path: str):
    # simple tail -f
    with open(path, "r", encoding="utf-8") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.strip()

def main():
    if not WEBHOOK:
        print("Set N8N_WEBHOOK env var to your n8n webhook URL.")
        return
    for line in tail(BUS):
        if not line:
            continue
        try:
            evt = json.loads(line)
        except Exception:
            continue
        try:
            requests.post(WEBHOOK, json=evt, timeout=5)
        except Exception:
            # optional: write to a local error log or retry queue
            pass

if __name__ == "__main__":
    main()
