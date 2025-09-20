import time

def now_ms():
    return int(time.time() * 1000)

def mode_set(memory, key, value):
    """Set mode and record timestamp if it changes."""
    m = memory.setdefault("_modes", {}).setdefault(key, {})
    if m.get("value") != value:
        m["value"] = value
        m["since"] = now_ms()

def elapsed_in_mode(memory, key, value):
    """Return ms elapsed since mode was set, else 0."""
    m = memory.get("_modes", {}).get(key, {})
    if m.get("value") != value:
        return 0
    return now_ms() - m.get("since", now_ms())

---

def op_mode_choose(memory, with_args):
    key = with_args["key"]              # e.g. "memory.anchor_mode"
    cases = with_args.get("cases", [])
    default_val = with_args.get("else")
    for case in cases:
        if eval_expr(case["when"], memory):   # use your safe expression evaluator
            mode_set(memory, key, case["value"])
            return
    if default_val is not None:
        mode_set(memory, key, default_val)

def op_mode_revert_after(memory, with_args):
    key = with_args["key"]
    value = with_args["value"]          # the mode to monitor, e.g. "learn"
    max_ms = int(eval_expr(str(with_args["max_ms"]), memory))
    if elapsed_in_mode(memory, key, value) >= max_ms:
        mode_set(memory, key, with_args.get("to", "hold"))
