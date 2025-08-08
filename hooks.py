# tastebuds/hooks.py
from typing import Dict, Any
from .common.flags import new_flag, write_flag

# ---- Generic emitter ----
def emit(source:str, event:str, *, severity:str="info", confidence:float=0.7, ttl_sec:int=3600, payload:Dict[str,Any]|None=None)->str:
    """Write a flag for Morgan to consume. Returns file path."""
    flag = new_flag(source=source, event=event, severity=severity, confidence=confidence, ttl_sec=ttl_sec, payload=payload)
    return write_flag(flag)

# ---- Agent-specific convenience wrappers ----
def jade_structure_support(event:str, **kw)->str:
    return emit("jade", event, **kw)

def morgan_forecast(event:str, **kw)->str:
    return emit("morgan", event, **kw)

def susanna_pre_tend(event:str, **kw)->str:
    return emit("susanna", event, **kw)

def ivy_escalation(event:str, **kw)->str:
    return emit("ivy", event, **kw)

def aspen_discovery(event:str, **kw)->str:
    return emit("aspen", event, **kw)

def sophie_saturation(event:str, **kw)->str:
    return emit("sophie", event, **kw)

# ---- Ready-made common events ----
def flag_saturation_spike(source:str, level:float, window:str="short", note:str="")->str:
    return emit(
        source,
        "saturation_spike",
        severity="warn" if level < 0.9 else "high",
        confidence=0.8,
        ttl_sec=1800,
        payload={"level": level, "window": window, "note": note},
    )

def flag_identity_melt(note:str="", confidence:float=0.85)->str:
    return sophie_saturation(
        "identity_melt_detected",
        severity="high",
        confidence=confidence,
        ttl_sec=1800,
        payload={"route_suggestion": "dissolution_maps/boundary_bloom.md", "note": note},
    )

def flag_escalation_needed(target:str, reason:str, confidence:float=0.75)->str:
    return ivy_escalation(
        "escalation_needed",
        severity="warn",
        confidence=confidence,
        ttl_sec=1200,
        payload={"target": target, "reason": reason},
    )
