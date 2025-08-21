#!/usr/bin/env python3
# Minimal metrics scorer (no deps). Usage examples:
#   python score.py --ease 2 --depth 1 --engage 2 --overheat 0 --stall 1
#   python score.py  # (interactive prompts)

import argparse

WEIGHTS = {
    "ease": 1.0,
    "depth": 1.2,
    "engage": 1.0,
    "overheat": -1.0,
    "stall": -0.6,
}

BANDS = [
    ("excellent", 3.5),
    ("healthy", 2.8),
    ("investigate", 2.0),
    ("poor", float("-inf")),
]

def compute_score(ease: int, depth: int, engage: int, overheat: int, stall: int) -> float:
    return (
        WEIGHTS["ease"] * ease
        + WEIGHTS["depth"] * depth
        + WEIGHTS["engage"] * engage
        + WEIGHTS["overheat"] * overheat
        + WEIGHTS["stall"] * stall
    )

def band(score: float) -> str:
    for name, threshold in BANDS:
        if score >= threshold:
            return name
    return "unknown"

def main():
    p = argparse.ArgumentParser(description="Compute emergent session score.")
    p.add_argument("--ease", type=int)
    p.add_argument("--depth", type=int)
    p.add_argument("--engage", type=int)
    p.add_argument("--overheat", type=int)
    p.add_argument("--stall", type=int)
    args = p.parse_args()

    vals = {}
    for k in ["ease","depth","engage","overheat","stall"]:
        v = getattr(args, k)
        if v is None:
            while True:
                try:
                    v = int(input(f"{k} (0/1/2): ").strip())
                    if v in (0,1,2):
                        break
                except Exception:
                    pass
                print("Please enter 0, 1, or 2.")
        vals[k] = v

    s = compute_score(**vals)
    print(f"score = {s:.2f}   →   {band(s)}")
    print("(formula: 1.0*ease + 1.2*depth + 1.0*engage - 1.0*overheat - 0.6*stall)")

if __name__ == "__main__":
    main()
