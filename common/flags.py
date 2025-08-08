# tastebuds/common/flags.py
import json, uuid, time, os
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
from .paths import morgan_flags_root, ensure_dir

@dataclass
class Flag:
    id: str
    source: str            # which tendril raised it (ivy, jade, sophie, susanna, aspen, morgan)
    event: str             # short machine name, e.g. "saturation_spike"
    severity: str          # "info" | "warn" | "high" | "critical"
    confidence: float      # 0..1
    created_at: float      # epoch seconds
    ttl_sec: int           # how long before worker can auto-archive
    status: str            # "open" | "acked" | "resolved"
    payload: Dict[str, Any]  # arbitrary metadata

SCHEMA_VERSION = "v1"

def new_flag(source:str, event:str, severity="info", confidence=0.7, ttl_sec=3600, payload:Optional[Dict[str,Any]]=None)->Flag:
    return Flag(
        id=str(uuid.uuid4()),
        source=source,
        event=event,
        severity=severity,
        confidence=confidence,
        created_at=time.time(),
        ttl_sec=int(ttl_sec),
        status="open",
        payload={"schema": SCHEMA_VERSION, **(payload or {})},
    )

def write_flag(flag: Flag) -> str:
    # path: morgan/flags/<source>/YYYYMMDD_<event>_<id>.json
    root = ensure_dir(morgan_flags_root(flag.source))
    ymd = time.strftime("%Y%m%d", time.gmtime(flag.created_at))
    fname = f"{ymd}_{flag.event}_{flag.id}.json"
    fpath = os.path.join(root, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(asdict(flag), f, ensure_ascii=False, indent=2)
    return fpath
