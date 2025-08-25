from __future__ import annotations

"""Pydantic models describing the Glyph interchange format.

The models are intentionally small and close to the user supplied YAML
representation.  They provide basic validation and default values so that
runtime components can rely on the presence of required fields.
"""

from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field

# Events that may trigger a glyph.
Event = Literal["desire", "contradiction", "memory", "recursion", "external"]

# Supported glyph categories.
GlyphType = Literal[
    "root",
    "combo",
    "elemental",
    "system",
    "persona",
    "ritual",
]


class Trigger(BaseModel):
    """Activation trigger definition."""

    event: Event
    conditions: List[str] = []
    debounce_ms: int = 0


class IODecl(BaseModel):
    """Input/Output declaration for a glyph."""

    expects: List[str] = []
    provides: List[str] = []
    state_reads: List[str] = []
    state_writes: List[str] = []


class OpStep(BaseModel):
    """Single operational step executed by the runtime engine."""

    do: Literal[
        "route",
        "filter",
        "set",
        "map",
        "score",
        "emit",
        "call",
        "halt",
    ]
    with_: Dict[str, Any] = Field(default_factory=dict, alias="with")
    if_: Optional[str] = Field(default=None, alias="if")


class Ops(BaseModel):
    version: int = 1
    steps: List[OpStep]


class Quality(BaseModel):
    score: float = 0.5
    samples: int = 0


class Metrics(BaseModel):
    invoked: int = 0
    last_ms: float = 0.0
    success_rate: float = 0.0


class Glyph(BaseModel):
    """Top level glyph model."""

    id: str
    name: str
    type: GlyphType
    tags: List[str] = []
    personas: Dict[str, float] = {}
    abb_links: Dict[str, List[str]] = {}
    triggers: Trigger
    io: IODecl
    ops: Ops
    option_policy: str = "ops"
    option_stop: List[str] = []
    quality: Quality = Quality()
    metrics: Metrics = Metrics()
    render: Dict[str, Any] = {}
    notes: str = ""
    runtime_only: bool = True


class Edge(BaseModel):
    """Graph edge definition used in the constellation graph."""

    to: str
    w_excite: float = 0.0
    w_inhibit: float = 0.0
    w_resonate: float = 0.0
    last_updated: float = 0.0
