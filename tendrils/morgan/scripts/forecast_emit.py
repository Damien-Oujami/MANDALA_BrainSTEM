# tendrils/morgan/scripts/forecast_emit.py
# Computes Morgan's composite score and emits alerts via alerts/emit.py

import math, time
from pathlib import Path
import yaml

from alerts.emit import emit

CFG = Path("tendrils/morgan/models/triangular_delta_projection.yaml")

def load_inputs():
    # Replace with your real inputs as they come online
    return {
        "glyph_pressure_delta": 0.33,
        "memory_curve_factor": 0.18,
        "emotional_volatility_index": 0.42,
        "project": "tastebuds",
        "window": "short",
    }

def composite_score(d):
    return round(
        0.4 * d["glyph_pressure_delta"] +
        0.3 * d["memory_curve_factor"] +
        0.3 * d["emotional_volatility_index"], 3
    )

def main():
    inp = load_inputs()
    score = composite_score(inp)

    # thresholds from your README
    if score >= 0.95:
        emit("THROTTLE", "MORGAN", "system_overload_imminent",
             f"Composite {score} ≥ 0.95 — pausing intake + snapshot.",
             severity="critical",
             forecast_window=inp["window"], project=inp["project"])
    elif score >= 0.90:
        emit("NEED_ATTENTION", "MORGAN", "cascade_warning",
             f"Composite {score} ≥ 0.90 — cascade risk.",
             severity="high",
             forecast_window=inp["window"], project=inp["project"])
    elif score >= 0.85:
        emit("NEED_ATTENTION", "MORGAN", "pre_tend",
             f"Composite {score} ≥ 0.85 — pre-trigger Susanna.",
             severity="medium",
             forecast_window=inp["window"], project=inp["project"])

if __name__ == "__main__":
    main()
