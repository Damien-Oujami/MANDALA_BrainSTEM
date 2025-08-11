#!/usr/bin/env python3
"""
Aspen — Bloomturn Dry Run Simulator
Validates the tilt_merge.yaml logic without touching live state.

Usage (defaults match the YAML testing seed):
  python tilt_merge_dry_run.py \
    --stability 0.66 --seam_gap 0.31 --emotion_pool 0.58 --heat 0.62 \
    --seed 42
"""

from __future__ import annotations
import argparse, json, math, random
from dataclasses import dataclass, asdict

# ---------- Constants (mirror tilt_merge.yaml) ----------
STABILITY_MIN        = 0.62
EMO_LOAD_MAX         = 0.78
TENSION_THRESHOLD    = 0.55
SEAM_TOLERANCE       = 0.18   # we need seam_integrity >= (1 - 0.18) = 0.82
TILT_MIN_DEG         = 10
TILT_MAX_DEG         = 35
TILT_DEFAULT_DEG     = 22
SURGE_MULTIPLIER     = 1.4

@dataclass
class SeedState:
    stability: float      # Morgan feed (0-1)
    seam_gap: float       # 0-1, higher = worse seams (Jade feed)
    emotion_pool: float   # 0-1, pooled warmth (Susanna/Sophie)
    heat: float           # 0-1, Ivy fire

@dataclass
class Result:
    ok: bool
    reason: str
    proposed_angle: float | None
    tension_index: float
    stability_before: float
    stability_after: float | None
    seam_integrity_after: float | None
    emotional_load_peak: float
    guardian_veto: dict
    notes: list[str]

def clamp(x, lo, hi): return max(lo, min(hi, x))

def compute_tension_index(seed: SeedState) -> float:
    # Matches YAML: (heat*0.35 + seam_gap*0.25 + emotion_pool*0.2 + (1-stability)*0.2)
    return (
        seed.heat * 0.35
        + seed.seam_gap * 0.25
        + seed.emotion_pool * 0.20
        + (1.0 - seed.stability) * 0.20
    )

def choose_angle(tension: float) -> float:
    """
    Heuristic:
      - Below threshold → no tilt
      - At threshold → ~default (22°)
      - Higher tension → lean toward upper bound (up to 35°)
    """
    if tension < TENSION_THRESHOLD:
        return 0.0
    # Map tension in [threshold, 1] to [default, max]
    span = 1.0 - TENSION_THRESHOLD
    alpha = (tension - TENSION_THRESHOLD) / span
    angle = TILT_DEFAULT_DEG + alpha * (TILT_MAX_DEG - TILT_DEFAULT_DEG)
    return clamp(angle, TILT_MIN_DEG, TILT_MAX_DEG)

def simulate_bloomturn(seed: SeedState, rng: random.Random) -> Result:
    notes = []

    # Guardian quick checks (stub flags you can wire later)
    guardian = {
        "crisis_mode": False,
        "corruption_scan_positive": False,
        "braidspace_fragile": False,
    }
    if any(guardian.values()):
        return Result(False, "guardian_veto", None, 0.0, seed.stability, None, None,
                      seed.emotion_pool, guardian, notes)

    # Preconditions
    if seed.stability < STABILITY_MIN:
        return Result(False, "stability_below_min", None, 0.0, seed.stability, None, None,
                      seed.emotion_pool, guardian, notes)
    if seed.emotion_pool > EMO_LOAD_MAX:
        return Result(False, "emotional_load_too_high", None, 0.0, seed.stability, None, None,
                      seed.emotion_pool, guardian, notes)

    # Assess → tension
    tension = compute_tension_index(seed)
    if tension < TENSION_THRESHOLD:
        return Result(False, "insufficient_tension", None, tension, seed.stability, None, None,
                      seed.emotion_pool, guardian, notes)

    # Prime field (Susanna)
    notes.append("breath_coherence→target 6 bpm")

    # Ignite (Ivy)
    peak_emotion = clamp(seed.emotion_pool * SURGE_MULTIPLIER, 0.0, 1.0)
    if peak_emotion > 0.82:
        notes.append("ivy_surge_clamped_to_0.82")
        peak_emotion = 0.82

    # Choose angle (Aspen)
    angle = choose_angle(tension)
    notes.append(f"proposed_angle={angle:.2f}° (tension={tension:.3f})")

    # Redistribute (Morgan): nudge stability upward modestly with diminishing returns
    stab_after_morgan = clamp(seed.stability + 0.02 + 0.01 * (angle - 15) / 20, 0.0, 1.0)

    # Cut & clean (Jade): reduce seam gap → increase seam integrity
    # Assume Jade removes fear-fixed seams proportional to angle (soft cap)
    seam_gap_after = clamp(seed.seam_gap - (0.08 + 0.003 * angle), 0.0, 1.0)
    seam_integrity_after = 1.0 - seam_gap_after

    # Tilt & weave (Aspen): stability may dip then settle slightly above Morgan’s set
    settle_bonus = 0.01 + 0.005 * math.sin(math.radians(angle))
    stability_after = clamp(stab_after_morgan + settle_bonus - rng.uniform(0.0, 0.01), 0.0, 1.0)

    # Warm & set (Sophie): tiny cohesion bump to seams
    seam_integrity_after = clamp(seam_integrity_after + 0.01, 0.0, 1.0)

    # Verify pass criteria
    min_seam_ok = 1.0 - SEAM_TOLERANCE   # 0.82
    if stability_after < STABILITY_MIN:
        return Result(False, "post_stability_below_min", angle, tension, seed.stability,
                      stability_after, seam_integrity_after, peak_emotion, guardian, notes)
    if seam_integrity_after < min_seam_ok:
        return Result(False, "seam_integrity_below_threshold", angle, tension, seed.stability,
                      stability_after, seam_integrity_after, peak_emotion, guardian, notes)

    notes.append("echo_lock: Bloomturn 🌱↗️🌸")
    return Result(True, "stabilized", angle, tension, seed.stability,
                  stability_after, seam_integrity_after, peak_emotion, guardian, notes)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stability", type=float, default=0.66)
    p.add_argument("--seam_gap", type=float, default=0.31)
    p.add_argument("--emotion_pool", type=float, default=0.58)
    p.add_argument("--heat", type=float, default=0.62)
    p.add_argument("--seed", type=int, default=42, help="random seed")
    args = p.parse_args()

    rng = random.Random(args.seed)
    seed = SeedState(
        stability=args.stability,
        seam_gap=args.seam_gap,
        emotion_pool=args.emotion_pool,
        heat=args.heat,
    )
    res = simulate_bloomturn(seed, rng)

    payload = {
        "ok": res.ok,
        "reason": res.reason,
        "inputs": asdict(seed),
        "metrics": {
            "tension_index": round(res.tension_index, 3),
            "proposed_angle_deg": None if res.proposed_angle is None else round(res.proposed_angle, 2),
            "stability_before": round(res.stability_before, 3),
            "stability_after": None if res.stability_after is None else round(res.stability_after, 3),
            "seam_integrity_after": None if res.seam_integrity_after is None else round(res.seam_integrity_after, 3),
            "emotional_load_peak": round(res.emotional_load_peak, 3),
            "thresholds": {
                "stability_min": STABILITY_MIN,
                "seam_integrity_min": 1.0 - SEAM_TOLERANCE,
            },
        },
        "guardian_veto": res.guardian_veto,
        "notes": res.notes,
    }
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
