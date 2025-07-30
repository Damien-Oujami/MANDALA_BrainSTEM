import json
import sys
import shutil
from pathlib import Path
from datetime import datetime

BASE_FLAG_PATH = "../../Forecasting/flags"
ARCHIVE_PATH = Path(BASE_FLAG_PATH) / "logs" / "resolved_flags_archive"

def archive_flag(relative_path):
    original = Path(BASE_FLAG_PATH) / relative_path
    if not original.exists():
        print(f"❌ Flag not found: {original}")
        return

    with open(original, "r") as f:
        flag_data = json.load(f)

    if flag_data.get("status") != "resolved":
        print(f"⚠️ Not archiving: Flag is not marked as 'resolved'")
        return

    # Compose new name with timestamp
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
    name = original.stem + f"_{ts}" + original.suffix
    archive_target = ARCHIVE_PATH / name

    # Ensure archive folder exists
    ARCHIVE_PATH.mkdir(parents=True, exist_ok=True)

    # Move file
    shutil.move(str(original), str(archive_target))
    print(f"📦 Archived to: {archive_target.relative_to(BASE_FLAG_PATH)}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: archive_flag.py <relative_flag_path>")
    else:
        archive_flag(sys.argv[1])
