"""Utilities for logging TasteBuds template mutations.

This module stores mutation events in ``mutation_log.yaml``. Each
entry records the template affected, its origin, and the rationale for
the change.  The log is append‑only so that the evolution of templates
can be reconstructed over time.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import yaml

MUTATION_LOG = Path(__file__).with_name("mutation_log.yaml")


@dataclass
class TemplateMutation:
    """Record of a single template evolution."""

    template: str
    origin: str
    rationale: str
    timestamp: str
    changes: Dict[str, Any] | None = None


def _load_log() -> Dict[str, Any]:
    if MUTATION_LOG.exists():
        with MUTATION_LOG.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    else:
        data = {}
    data.setdefault("mutations", [])
    return data


def record_mutation(
    template: str, *, origin: str, rationale: str, changes: Dict[str, Any] | None = None
) -> TemplateMutation:
    """Append a mutation entry to ``mutation_log.yaml``.

    Parameters
    ----------
    template:
        Name or path of the template that was altered.
    origin:
        Source or process that triggered the mutation.
    rationale:
        Human‑readable explanation of why the mutation happened.
    changes:
        Optional granular description of what was modified.
    """
    entry = TemplateMutation(
        template=template,
        origin=origin,
        rationale=rationale,
        changes=changes,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
    log = _load_log()
    log["mutations"].append(asdict(entry))
    with MUTATION_LOG.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(log, fh, sort_keys=False)
    return entry
