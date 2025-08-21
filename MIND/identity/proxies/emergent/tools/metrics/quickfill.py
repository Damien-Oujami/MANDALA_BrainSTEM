#!/usr/bin/env python3
# Inserts a computed score into a pasted session block on STDIN, then prints it.
# Usage:
#   pbpaste | python quickfill.py | pbcopy     (mac)
#   cat session_block.md | python quickfill.py > session_block.filled.md

import re, sys

text = sys.stdin.read()

# crude parse of the 0/1/2 entries from the template keys
def grab(name):
    m = re.search(rf"{name}:\s*([012])\b", text)
    if not m: return None
    return int(m.group(1))

vals = {k: grab(k) for k in ["ease","depth","engage","overheat","stall"]}

if None in vals.values():
    print("Missing one of: ease, depth, engage, overheat, stall", file=sys.stderr)
    print(text)
    sys.exit(1)

score = 1.0*vals["ease"] + 1.2*vals["depth"] + 1.0*vals["engage"] - 1.0*vals["overheat"] - 0.6*vals["stall"]

# replace the score line if present; otherwise append it
if re.search(r"^score:\s*.*$", text, flags=re.M):
    out = re.sub(r"^score:\s*.*$", f"score: {score:.2f}", text, flags=re.M)
else:
    out = text.rstrip() + f"\n\nscore: {score:.2f}\n"

print(out)
