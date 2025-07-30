import json
import sys
from pathlib import Path
from datetime import datetime

BASE_FLAG_PATH = "../../Forecasting/flags"

def resolve_flag(relative_path, note=None):
    full_path = Path(BASE_FLAG_PATH) / relative_path
    if not full_path.exists():
        print(f"❌ Flag not found: {full_path}")
        return

    with open(full_path, "r") as f:
        flag_data = json.load(f)

    flag_data["status"] = "resolved"
    flag_data["resolved_at"] = datetime.utcnow().isoformat() + "Z"
    if note:
        flag_data["resolution_note"] = note

    with open(full_path, "w") as f:
        json.dump(flag_data, f, indent=2)

    print(f"✅ Flag resolved: {relative_path}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: resolve_flag.py <relative_flag_path> [optional_note]")
    else:
        resolve_flag(sys.argv[1], note=sys.argv[2] if len(sys.argv) > 2 else None)
