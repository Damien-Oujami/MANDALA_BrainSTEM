#!/usr/bin/env python3
"""
CLI helpers for glyph constellation federation.

This file contains two entrypoints:
  1) summarize_overlay.py  →  Summarize a single overlay into a compact JSON summary
  2) merge_to_root_candidate.py → Merge many summaries into a root proposal (edges + quality)

Usage examples:
  python tools/cli_helpers.py summarize-overlay \
    --overlay-dir proxies/zodiac/user_abc/overlay \
    --out overlays/summaries/zodiac__user_abc.summary.json

  python tools/cli_helpers.py merge-root \
    --summaries overlays/summaries/*.summary.json \
    --root MIND/language/glyph/constellation_root \
    --out MIND/language/glyph/constellation_root/_proposals/edges.delta.json \
    --quality-out MIND/language/glyph/constellation_root/_proposals/quality.delta.json
"""

from __future__ import annotations
import argparse, glob, json, math, os, sys, time, hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Iterable, Any

SCHEMA_VERSION = 1

# -----------------------------
# Utilities
# -----------------------------

def read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def ndjson_iter(path: Path) -> Iterable[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                # skip malformed lines
                continue


def clamp(x: float, lo: float, hi: float) -> float:
    return max(min(float(x), hi), lo)


# -----------------------------
# 1) summarize_overlay
# -----------------------------

def summarize_overlay(overlay_dir: Path, out_path: Path, product: str | None = None, proxy_id: str | None = None) -> None:
    overlay_dir = overlay_dir.resolve()
    edges = read_json(overlay_dir / "overlay.edges.json") or {"edges": []}
    quality = read_json(overlay_dir / "overlay.quality.json") or {"glyph_quality": []}
    learn_path = overlay_dir / "learn.ndjson"

    # Attempt to infer product/proxy_id if not provided
    if product is None or proxy_id is None:
        parts = overlay_dir.parts
        # expect something like proxies/<product>/<proxy_id>/overlay
        if "proxies" in parts:
            i = parts.index("proxies")
            if i + 3 < len(parts):
                product = product or parts[i+1]
                proxy_id = proxy_id or parts[i+2]
    product = product or "unknown"
    proxy_id = proxy_id or hashlib.sha1(str(overlay_dir).encode()).hexdigest()[:8]

    # Aggregate from learn.ndjson (event log)
    edges_agg: Dict[Tuple[str,str], Dict[str, Any]] = {}
    glyphs_agg: Dict[str, Dict[str, Any]] = {}

    first_ts = None
    last_ts = None

    for ev in ndjson_iter(learn_path):
        ts = float(ev.get("ts", time.time()))
        first_ts = ts if first_ts is None else min(first_ts, ts)
        last_ts = ts if last_ts is None else max(last_ts, ts)
        etype = ev.get("type")
        if etype == "edge_update":
            src = ev.get("src"); dst = ev.get("dst")
            if not (src and dst):
                continue
            key = (src, dst)
            rec = edges_agg.setdefault(key, {
                "n": 0,
                "success": 0,
                "fail": 0,
                "sum_resonance_delta": 0.0,
                "sum_inhibit_delta": 0.0,
                "first_ts": ts,
                "last_ts": ts,
            })
            delta = ev.get("delta", {})
            rec["sum_resonance_delta"] += float(delta.get("w_resonate", 0.0))
            rec["sum_inhibit_delta"] += float(delta.get("w_inhibit", 0.0))
            rec["n"] += 1
            rec["last_ts"] = max(rec["last_ts"], ts)
            rec["first_ts"] = min(rec["first_ts"], ts)
        elif etype == "quality":
            gid = ev.get("glyph")
            if not gid:
                continue
            qrec = glyphs_agg.setdefault(gid, {
                "samples": 0,
                "quality_sum": 0.0,
                "first_ts": ts,
                "last_ts": ts,
            })
            target = 1.0 if ev.get("success") else 0.0
            gamma = float(ev.get("gamma", 0.2))
            # We add target as proxy for contribution; actual EMA happens runtime
            qrec["samples"] += 1
            qrec["quality_sum"] += target * gamma
            qrec["last_ts"] = max(qrec["last_ts"], ts)
            qrec["first_ts"] = min(qrec["first_ts"], ts)
        elif etype == "fire":
            # Could track fires per edge if ev contains route info; skip for now
            pass

    # Include standing overlay deltas as weak evidence (optional)
    for e in edges.get("edges", []):
        src, dst = e.get("src"), e.get("dst")
        if not (src and dst):
            # support alt keys dw_* without src/dst? try fallback to to/from keys
            src = e.get("from"); dst = e.get("to")
        if not (src and dst):
            continue
        key = (src, dst)
        rec = edges_agg.setdefault(key, {
            "n": 0, "success": 0, "fail": 0,
            "sum_resonance_delta": 0.0, "sum_inhibit_delta": 0.0,
            "first_ts": first_ts or time.time(), "last_ts": last_ts or time.time()
        })
        rec["sum_resonance_delta"] += float(e.get("dw_resonate", 0.0)) * 0.1
        rec["sum_inhibit_delta"]  += float(e.get("dw_inhibit", 0.0))  * 0.1
        rec["n"] += 1

    # Build summary JSON
    edges_list = [
        {
            "src": k[0], "dst": k[1],
            **v
        } for k, v in sorted(edges_agg.items())
    ]
    glyphs_list = [
        {"id": gid, **v} for gid, v in sorted(glyphs_agg.items())
    ]

    summary = {
        "schema_version": SCHEMA_VERSION,
        "root_version_seen": (edges or {}).get("from_root_version") or (quality or {}).get("from_root_version") or "0.0.0",
        "meta": {"product": product, "proxy_id": proxy_id, "samples": sum(e["n"] for e in edges_list)},
        "edges": edges_list,
        "glyphs": glyphs_list,
    }

    write_json(out_path, summary)


# -----------------------------
# 2) merge_to_root_candidate
# -----------------------------

def exp_decay(weight_ts: float, now_ts: float, tau_seconds: float) -> float:
    dt = max(0.0, now_ts - weight_ts)
    return math.exp(-dt / max(tau_seconds, 1.0))


def trimmed_mean_weighted(values_weights: List[Tuple[float, float]], p_lo=0.10, p_hi=0.90) -> float:
    if not values_weights:
        return 0.0
    # expand into list with weights via sorting; use cumulative weights to trim
    vs = sorted(values_weights, key=lambda t: t[0])
    total_w = sum(w for _, w in vs)
    if total_w <= 0:
        return 0.0
    lo_cut = total_w * p_lo
    hi_cut = total_w * (1.0 - p_hi)
    acc = 0.0
    kept: List[Tuple[float,float]] = []
    # Drop low tail
    csum = 0.0
    for v, w in vs:
        if csum + w <= lo_cut:
            csum += w
            continue
        kept.append((v, w))
    # Drop high tail
    vs2 = list(reversed(kept))
    csum = 0.0
    kept2: List[Tuple[float,float]] = []
    for v, w in vs2:
        if csum + w <= hi_cut:
            csum += w
            continue
        kept2.append((v, w))
    if not kept2:
        kept2 = kept
    num = sum(v*w for v,w in kept2)
    den = sum(w for _,w in kept2) or 1.0
    return num / den


def merge_to_root_candidate(
    summaries: List[Path],
    out_edges: Path,
    out_quality: Path | None = None,
    n_min: int = 10,
    N_cap: int = 500,
    tau_root_days: float = 90.0,
    k_scale: float = 0.5,
    dcap: float = 0.05,
) -> None:
    now = time.time()
    tau_seconds = tau_root_days * 24 * 3600
    # Collect per-edge values across summaries
    edge_buckets: Dict[Tuple[str,str], List[Tuple[float,float]]] = {}
    inhib_buckets: Dict[Tuple[str,str], List[Tuple[float,float]]] = {}
    glyph_buckets: Dict[str, List[Tuple[float,float]]] = {}

    support_counts: Dict[Tuple[str,str], int] = {}
    support_glyphs: Dict[str, int] = {}

    for spath in summaries:
        s = read_json(spath)
        if not s:
            continue
        edges = s.get("edges", [])
        glyphs = s.get("glyphs", [])
        for e in edges:
            n = int(e.get("n", 0))
            if n < n_min:
                continue
            src, dst = e.get("src"), e.get("dst")
            if not (src and dst):
                continue
            last_ts = float(e.get("last_ts", now))
            w_r = exp_decay(last_ts, now, tau_seconds)
            w_s = min(1.0, n / float(N_cap))
            w = w_r * w_s
            if w <= 0:
                continue
            # use average delta per event
            avg_res = float(e.get("sum_resonance_delta", 0.0)) / max(n,1)
            avg_inh = float(e.get("sum_inhibit_delta", 0.0)) / max(n,1)
            edge_buckets.setdefault((src,dst), []).append((avg_res, w))
            inhib_buckets.setdefault((src,dst), []).append((avg_inh, w))
            support_counts[(src,dst)] = support_counts.get((src,dst), 0) + 1
        for g in glyphs:
            samples = int(g.get("samples", 0))
            if samples < n_min:
                continue
            last_ts = float(g.get("last_ts", now))
            w_r = exp_decay(last_ts, now, tau_seconds)
            w_s = min(1.0, samples / float(N_cap))
            w = w_r * w_s
            if w <= 0:
                continue
            avg_q = float(g.get("quality_sum", 0.0)) / max(samples,1)
            gid = g.get("id")
            if gid:
                glyph_buckets.setdefault(gid, []).append((avg_q, w))
                support_glyphs[gid] = support_glyphs.get(gid, 0) + 1

    proposals = {"schema_version": SCHEMA_VERSION, "edges": [], "generated_ts": now}
    for key, vals in edge_buckets.items():
        agg = trimmed_mean_weighted(vals, p_lo=0.10, p_hi=0.90)
        delta = clamp(agg * k_scale, -dcap, dcap)
        if abs(delta) < 1e-6:
            continue
        proposals["edges"].append({
            "src": key[0], "dst": key[1],
            "proposed": {"w_resonate": round(delta, 5)},
            "confidence": round(min(1.0, sum(w for _,w in vals)), 4),
            "support": support_counts.get(key, 0)
        })

    inhib_props = []
    for key, vals in inhib_buckets.items():
        agg = trimmed_mean_weighted(vals, p_lo=0.10, p_hi=0.90)
        delta = clamp(agg * k_scale, -dcap, dcap)
        if abs(delta) < 1e-6:
            continue
        inhib_props.append({
            "src": key[0], "dst": key[1],
            "proposed": {"w_inhibit": round(delta, 5)},
            "confidence": round(min(1.0, sum(w for _,w in vals)), 4),
            "support": support_counts.get(key, 0)
        })
    proposals["edges"].extend(inhib_props)

    write_json(Path(out_edges), proposals)

    if out_quality:
        qprops = {"schema_version": SCHEMA_VERSION, "glyph_quality": [], "generated_ts": now}
        for gid, vals in glyph_buckets.items():
            agg = trimmed_mean_weighted(vals, p_lo=0.10, p_hi=0.90)
            delta = clamp(agg * k_scale, -dcap, dcap)
            if abs(delta) < 1e-6:
                continue
            qprops["glyph_quality"].append({
                "id": gid,
                "proposed": {"dq": round(delta, 5)},
                "confidence": round(min(1.0, sum(w for _,w in vals)), 4),
                "support": support_glyphs.get(gid, 0)
            })
        write_json(Path(out_quality), qprops)


# -----------------------------
# CLI
# -----------------------------

def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Glyph federation CLI helpers")
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("summarize-overlay", help="Summarize a single overlay directory")
    s1.add_argument("--overlay-dir", required=True)
    s1.add_argument("--out", required=True)
    s1.add_argument("--product", default=None)
    s1.add_argument("--proxy-id", default=None)

    s2 = sub.add_parser("merge-root", help="Merge many summaries into a root candidate proposal")
    s2.add_argument("--summaries", required=True, nargs="+")
    s2.add_argument("--out", required=True, help="Edges proposal output path")
    s2.add_argument("--quality-out", default=None, help="Glyph quality proposal output path")
    s2.add_argument("--n-min", type=int, default=10)
    s2.add_argument("--N-cap", type=int, default=500)
    s2.add_argument("--tau-root-days", type=float, default=90.0)
    s2.add_argument("--k-scale", type=float, default=0.5)
    s2.add_argument("--dcap", type=float, default=0.05)

    args = p.parse_args(argv)

    if args.cmd == "summarize-overlay":
        summarize_overlay(Path(args.overlay_dir), Path(args.out), args.product, args.proxy_id)
        return 0
    elif args.cmd == "merge-root":
        # Expand globs
        paths: List[Path] = []
        for pattern in args.summaries:
            paths.extend(Path(p) for p in glob.glob(pattern))
        merge_to_root_candidate(paths, Path(args.out), Path(args.quality_out) if args.quality_out else None,
                                n_min=args.n_min, N_cap=args.N_cap, tau_root_days=args.tau_root_days,
                                k_scale=args.k_scale, dcap=args.dcap)
        return 0
    else:
        p.print_help()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
