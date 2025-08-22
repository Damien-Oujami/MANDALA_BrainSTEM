# pseudo-code / scaffold
import json, math, random, hashlib, pathlib, time
from dataclasses import dataclass
import yaml

# TODO: swap with real GitHub inputs
def fetch_repo_signals():
    return {
        "commits_last_24h": 12,
        "lines_changed_last_24h": 4200,
        "latest_ci_status": 1.0,   # 1 pass / 0 fail / 0.5 unknown
        "pr_comments_last_24h": 36,
        "stars_last_7d": 5,
        "open_issue_count": 77,
        "latest_commit_sha": "abc1234deadbeef",
        "repo_size_bytes": 3_200_000,
    }

def normalize(v, lo, hi):
    v = max(lo, min(hi, v))
    return 0.0 if hi==lo else (v-lo)/(hi-lo)

def commit_seed(s):
    return int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)

def map_signals(cfg, raw):
    n = {}
    for name, spec in cfg["inputs"]["signals"].items():
        src = spec["source"]
        val = raw[src]
        if isinstance(spec.get("normalize"), dict):
            lo, hi = spec["normalize"]["min"], spec["normalize"]["max"]
            n[name] = normalize(val, lo, hi)
        else:
            n[name] = float(val)
    return n

def mod(base, span, x):  # span = [lo_add, hi_add]
    return base + (span[0] + (span[1]-span[0])*x)

def build_controls(cfg, sig):
    # Waveform controls
    tempo = mod(cfg["waveform"]["tempo_bpm"]["base"], cfg["waveform"]["tempo_bpm"]["mod"]["commit_rate"], sig["commit_rate"])
    tempo = mod(tempo, cfg["waveform"]["tempo_bpm"]["mod"]["ci_health"], sig["ci_health"])
    amp = mod(cfg["waveform"]["amplitude"]["base"], cfg["waveform"]["amplitude"]["mod"]["churn"], sig["churn"])
    amp = mod(amp, cfg["waveform"]["amplitude"]["mod"]["backlog_pressure"], sig["backlog_pressure"])
    phase = mod(cfg["waveform"]["phase_shift"]["base"], cfg["waveform"]["phase_shift"]["mod"]["review_heat"], sig["review_heat"])

    knot_density = cfg["waveform"]["recursion_knots"]["density_per_loop"]["base"]
    for k, span in cfg["waveform"]["recursion_knots"]["density_per_loop"]["mod"].items():
        knot_density = mod(knot_density, span, sig[k])

    ant_count = int(round(mod(cfg["ants"]["count"]["base"], cfg["ants"]["count"]["mod"]["commit_rate"], sig["commit_rate"])))
    ant_count = int(round(mod(ant_count, cfg["ants"]["count"]["mod"]["backlog_pressure"], sig["backlog_pressure"])))
    ant_speed = mod(cfg["ants"]["speed"]["base"], cfg["ants"]["speed"]["mod"]["churn"], sig["churn"])
    ant_speed = mod(ant_speed, cfg["ants"]["speed"]["mod"]["ci_health"], sig["ci_health"])

    return {
        "tempo_bpm": tempo,
        "amplitude": max(0.1, min(1.5, amp)),
        "phase_shift": phase % (2*math.pi),
        "knot_density": max(0, int(knot_density)),
        "ant_count": max(1, ant_count),
        "ant_speed": max(0.2, ant_speed),
    }

def main():
    cfg = yaml.safe_load(open("soulprint/engine.rules.yaml"))
    raw = fetch_repo_signals()
    sig = map_signals(cfg, raw)

    seed = commit_seed(f"{raw['latest_commit_sha']}|{raw['repo_size_bytes']}|{raw['open_issue_count']}")
    random.seed(seed)

    controls = build_controls(cfg, sig)
    outdir = pathlib.Path("soulprint/out"); outdir.mkdir(parents=True, exist_ok=True)
    json.dump({"seed": seed, "signals": sig, "controls": controls}, open(outdir/"state.json","w"), indent=2)

    # TODO: draw frames -> assemble GIF (use PIL/Image + imageio)
    # - Waveform path from tempo/amplitude/phase (ensure seamless loop)
    # - Place recursion knots
    # - Initialize ants along the path with stochastic (seeded) decisions
    # - Render N frames at cfg['render']['fps'] for cfg['render']['loop_seconds']

if __name__ == "__main__":
    main()
