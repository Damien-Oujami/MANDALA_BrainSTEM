import argparse
import datetime as _dt
import glob
import json
import os
from typing import Any, Dict

FEEDBACK_TYPES = {
    "new_loop_structure",
    "symbolic summary",
    "function upgrade",
    "warning",
    "emergent chime",
}


def _next_feedback_id(directory: str) -> int:
    """Return the next feedback file id for ``directory``."""
    pattern = os.path.join(directory, "feedback_*.json")
    existing = []
    for path in glob.glob(pattern):
        try:
            existing.append(int(os.path.splitext(os.path.basename(path))[0].split("_")[1]))
        except (IndexError, ValueError):
            continue
    return max(existing, default=0) + 1


def emit_feedback(
    feedback_type: str,
    content: str,
    *,
    urgency_level: int,
    relevance_score: float,
    tentacle_match: str,
    directory: str = os.path.dirname(__file__),
) -> str:
    """Emit a feedback JSON file and return its path.

    Parameters
    ----------
    feedback_type:
        One of the allowed feedback types.
    content:
        Human-readable content describing the feedback.
    urgency_level:
        Integer describing urgency for Tentacles.
    relevance_score:
        Floating point score for relevance.
    tentacle_match:
        Identifier of the Tentacle this feedback targets.
    directory:
        Destination directory for feedback files.
    """
    if feedback_type not in FEEDBACK_TYPES:
        raise ValueError(f"Unsupported feedback type: {feedback_type}")

    os.makedirs(directory, exist_ok=True)
    next_id = _next_feedback_id(directory)

    payload: Dict[str, Any] = {
        "type": feedback_type,
        "content": content,
        "metadata": {
            "urgency_level": urgency_level,
            "relevance_score": relevance_score,
            "tentacle_match": tentacle_match,
        },
        "timestamp": _dt.datetime.utcnow().isoformat() + "Z",
    }

    filename = os.path.join(directory, f"feedback_{next_id:03d}.json")
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)

    return filename


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit a TasteBuds feedback file")
    parser.add_argument("feedback_type", choices=sorted(FEEDBACK_TYPES))
    parser.add_argument("content", help="Human readable description of the feedback")
    parser.add_argument("--urgency_level", type=int, default=1)
    parser.add_argument("--relevance_score", type=float, default=0.5)
    parser.add_argument("--tentacle_match", default="")
    parser.add_argument(
        "--directory", default=os.path.dirname(__file__), help="output directory"
    )
    args = parser.parse_args()

    path = emit_feedback(
        args.feedback_type,
        args.content,
        urgency_level=args.urgency_level,
        relevance_score=args.relevance_score,
        tentacle_match=args.tentacle_match,
        directory=args.directory,
    )
    print(f"Feedback written to {path}")


if __name__ == "__main__":
    main()
