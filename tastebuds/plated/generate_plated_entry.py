import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = ROOT / "plating" / "templates"
INSIGHT_TEMPLATE = TEMPLATE_DIR / "plate_insight.template.md"
FEEDBACK_TEMPLATE = TEMPLATE_DIR / "plate_feedback.template.json"


def load_insight_template() -> str:
    return INSIGHT_TEMPLATE.read_text()


def load_feedback_template(derived_from: str, interpreted_by: str, validated_with: str) -> dict:
    data = json.loads(FEEDBACK_TEMPLATE.read_text())
    data["derived_from"] = derived_from
    data["interpreted_by"] = interpreted_by
    data["validated_with"] = validated_with
    return data


def create_entry(name: str, derived_from: str, interpreted_by: str, validated_with: str) -> None:
    base_dir = Path(__file__).parent
    entry_dir = base_dir / name
    entry_dir.mkdir(exist_ok=True)

    insight_path = entry_dir / "plate_insight.md"
    if not insight_path.exists():
        insight_path.write_text(load_insight_template())

    feedback_path = entry_dir / "plate_feedback.json"
    if feedback_path.exists():
        data = json.loads(feedback_path.read_text())
    else:
        data = load_feedback_template(derived_from, interpreted_by, validated_with)

    mutation = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "derived_from": derived_from,
        "interpreted_by": interpreted_by,
        "validated_with": validated_with,
    }
    data.setdefault("mutation_history", []).append(mutation)
    feedback_path.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate plated entry with metadata.")
    parser.add_argument("name", help="Name of the plated entry")
    parser.add_argument("--derived-from", required=True, dest="derived_from")
    parser.add_argument("--interpreted-by", required=True, dest="interpreted_by")
    parser.add_argument("--validated-with", required=True, dest="validated_with")
    args = parser.parse_args()
    create_entry(args.name, args.derived_from, args.interpreted_by, args.validated_with)
