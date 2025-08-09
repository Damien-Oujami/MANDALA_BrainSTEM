# alerts/notifier.py
import time, json, requests, os

WEBHOOK = os.getenv("N8N_WEBHOOK")  # e.g. https://n8n.example/webhook/brainstem-alert
BUS = "alerts/events.jsonl"

def tail(path):
    with open(path, "r", encoding="utf-8") as f:
        f.seek(0,2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5); continue
            yield line.strip()

def main():
    for line in tail(BUS):
        if not line: continue
        try:
            evt = json.loads(line)
        except Exception:
            continue
        try:
            requests.post(WEBHOOK, json=evt, timeout=5)
        except Exception:
            # Optional: write to alerts/notifier_errors.log
            pass

if __name__ == "__main__":
    main()
