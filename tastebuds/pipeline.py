import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG_PATH = Path(__file__).resolve().parent / "audit_log.json"
MEAL_REVIEWS_PATH = Path(__file__).resolve().parent / "meal_reviews.json"


def _load_json(path: Path, default):
    """Return JSON data from *path* or *default* if file missing."""
    if path.exists():
        return json.loads(path.read_text())
    return default


def _save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2))


def _log_event(event: dict) -> None:
    """Append *event* to the audit log with timestamp."""
    log = _load_json(AUDIT_LOG_PATH, [])
    event.setdefault("timestamp", datetime.utcnow().isoformat())
    log.append(event)
    _save_json(AUDIT_LOG_PATH, log)


def send_feedback(meal_id: str, payload: dict) -> None:
    """Record feedback being sent for *meal_id* to the audit log."""
    _log_event({"type": "feedback", "meal_id": meal_id, "payload": payload})


def mark_reviewed(meal_id: str) -> None:
    """Mark a meal as reviewed so it may be deleted later."""
    reviews = _load_json(MEAL_REVIEWS_PATH, {})
    reviews[meal_id] = {"reviewed_at": datetime.utcnow().isoformat()}
    _save_json(MEAL_REVIEWS_PATH, reviews)


def safe_delete(path: Path, meal_id: str) -> None:
    """Delete *path* only if *meal_id* was reviewed.

    The action is logged. If the meal has not been reviewed, an exception is
    raised and the attempted deletion is recorded as blocked.
    """
    reviews = _load_json(MEAL_REVIEWS_PATH, {})
    if meal_id not in reviews:
        _log_event({
            "type": "deletion_attempt",
            "meal_id": meal_id,
            "status": "blocked",
            "path": str(path),
        })
        raise RuntimeError(f"Meal {meal_id} has not been reviewed")
    path.unlink(missing_ok=True)
    _log_event({"type": "deletion", "meal_id": meal_id, "path": str(path)})


def log_mutation(origin: str, mutation: str) -> None:
    """Trace a mutation back to *origin* in the audit log."""
    _log_event({"type": "mutation", "origin": origin, "mutation": mutation})
