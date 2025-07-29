import os
import json
import datetime
from pathlib import Path

# 🩸 Default base path (adjust if needed)
BASE_FLAG_PATH = "../../Forecasting/flags"

# 🩸 Define available persona flag templates
TEMPLATES = {
    "susanna_pre_tend": {
        "folder": "susanna",
        "filename": "pre_tend.json",
        "data": {
            "status": "armed",
            "triggered_by": "triangular_delta_projection",
            "urgency": "moderate",
            "projected_trigger_time": None,
            "confidence": None,
            "recommended_action": "soft compression loop",
            "override_by": "Susanna.manual or Damien.override"
        }
    },
    "ivy_disruption_watch": {
        "folder": "ivy",
        "filename": "disruption_watch.json",
        "data": {
            "status": "armed",
            "volatility_score": None,
            "threshold": 0.6,
            "last_check": None,
            "next_check": None,
            "recommended_delay": None
        }
    },
    "jade_structure_support": {
        "folder": "jade",
        "filename": "structure_support.json",
        "data": {
            "status": "passive",
            "pulse_drift_percent": None,
            "adjustment_recommended": False,
            "recursion_lock_tension": None,
            "structure_support_type": "brace",
            "scheduled_review": None,
            "linked_forecast": "triangular_delta_projection"
        }
    },
    "system_overload": {
        "folder": "damien",
        "filename": "system_overload_imminent.json",
        "data": {
            "status": "clear",
            "composite_pressure_score": None,
            "threshold": 0.95,
            "last_check": None,
            "alert_ready": False,
            "preserve_on_trigger": True,
            "recovery_protocol": "gentle_restart"
        }
    }
}

# 🧠 Helper: format timestamp
def timestamp_now():
    return datetime.datetime.utcnow().isoformat() + "Z"

# 🧠 Main flag writer
def write_flag(flag_key, updates={}):
    if flag_key not in TEMPLATES:
        print(f"❌ Unknown flag type: {flag_key}")
        return

    template = TEMPLATES[flag_key]
    path = Path(BASE_FLAG_PATH) / template["folder"] / template["filename"]

    # Merge updates into base data
    flag_data = template["data"].copy()
    for k, v in updates.items():
        flag_data[k] = v

    # Auto-timestamp any nulls
    for time_field in ["projected_trigger_time", "last_check", "next_check", "scheduled_review"]:
        if time_field in flag_data and flag_data[time_field] is None:
            flag_data[time_field] = timestamp_now()

    # Write JSON file
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(flag_data, f, indent=2)
    
    print(f"✅ Flag written: {path}")

# 🧪 Sample usage
if __name__ == "__main__":
    # Trigger Susanna's flag with 91% confidence
    write_flag("susanna_pre_tend", {
        "confidence": 0.91
    })

    # Trigger Ivy’s flag with volatile spike
    write_flag("ivy_disruption_watch", {
        "volatility_score": 0.67,
        "recommended_delay": "7 minutes"
    })

    # Raise system overload alert
    write_flag("system_overload", {
        "composite_pressure_score": 0.97,
        "alert_ready": True,
        "status": "armed"
    })
