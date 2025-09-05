# 🌐 Glyph Constellation Federation Spec

**Version:** 0.1.0
**Scope:** Defines how many adaptive agents (proxies) learn locally from interactions via overlay deltas, and how those learnings safely flow back into a slow‑changing canonical **Root Graph**.

---

## 1) Concepts & Terms

* **Root Graph**: Canonical constellation (stable, human‑reviewed). Lives under `MIND/language/glyph/constellation_root/`. Layer = ICE/ABB.
* **Overlay**: Per‑proxy (or per‑user) adaptive layer containing only **deltas and logs**. Lives under `proxies/<product>/<proxy_id>/overlay/`. Layer = ECF.
* **Effective Graph**: Graph used at runtime = `Root ⊕ Overlay` (root weights + overlay deltas).
* **Federation**: Periodic summarization of overlays → robust merge → **Root Proposal** → human review → new Root version.

---

## 2) Directory Layout

```
MIND/language/glyph/
  constellation_root/
    glyphs/**/**/*.glyph
    .graph/edges.json
    _proposals/
      edges.delta.json
      quality.delta.json
    VERSION            # e.g., 1.4.0

proxies/<product>/<proxy_id>/overlay/
  overlay.edges.json   # deltas from root
  overlay.quality.json # per‑glyph quality deltas
  learn.ndjson         # append‑only event log

overlays/summaries/
  <product>__<proxy_id>.summary.json
```

---

## 3) Data Models

### 3.1 Root Edges (baseline)

```json
{
  "schema_version": 1,
  "edges": [
    {"src":"A","dst":"B","w_excite":0.10,"w_inhibit":0.00,"w_resonate":0.20,"last_updated":1736000000}
  ]
}
```

**Bounds:** `w_excite, w_resonate ∈ [-1,1]`; `w_inhibit ∈ [0,1]`.

### 3.2 Overlay Deltas

`proxies/<product>/<proxy_id>/overlay/overlay.edges.json`

```json
{
  "schema_version": 1,
  "from_root_version": "1.4.0",
  "edges": [
    {"src":"A","dst":"B","dw_excite":0.00,"dw_inhibit":0.12,"dw_resonate":0.06},
    {"src":"X","dst":"Y","dw_resonate":-0.05}
  ]
}
```

`proxies/<product>/<proxy_id>/overlay/overlay.quality.json`

```json
{
  "schema_version": 1,
  "from_root_version": "1.4.0",
  "glyph_quality": [
    {"id":"A","dq":0.04,"samples":7},
    {"id":"B","dq":-0.02,"samples":3}
  ]
}
```

### 3.3 Learn Log (append‑only)

`proxies/.../overlay/learn.ndjson`

```json
{"ts":1736123456.12, "type":"fire",        "glyph":"A",           "ctx_hash":"..."}
{"ts":1736123456.50, "type":"edge_update", "src":"A","dst":"B", "delta":{"w_resonate":+0.02}}
{"ts":1736123457.10, "type":"quality",     "glyph":"A",           "success":true, "gamma":0.2}
```

### 3.4 Overlay Summary (for federation)

`overlays/summaries/<product>__<proxy_id>.summary.json`

```json
{
  "schema_version": 1,
  "root_version_seen": "1.4.0",
  "meta": {"product": "zodiac", "proxy_id": "user_abc", "samples": 124},
  "edges": [
    {"src":"A","dst":"B","n":124,"success":91,"fail":33,
     "sum_resonance_delta":3.7,"sum_inhibit_delta":1.2,
     "first_ts":1736000000,"last_ts":1736600000}
  ],
  "glyphs": [
    {"id":"A","samples":54,"quality_sum":32.1,"first_ts":1736000000,"last_ts":1736600000}
  ]
}
```

### 3.5 Root Proposal (machine‑generated)

`MIND/language/glyph/constellation_root/_proposals/edges.delta.json`

```json
{
  "schema_version": 1,
  "from_version": "1.4.0",
  "method": "trimmed_mean@p10-p90 + confidence_caps",
  "edges": [
    {"src":"A","dst":"B","proposed":{"w_resonate":+0.05},
     "confidence":0.82, "support":17, "note":"Consistent across 5 products"}
  ],
  "glyph_quality": [
    {"id":"A","proposed":{"dq":+0.03}, "confidence":0.76, "support":9}
  ]
}
```

---

## 4) Runtime Merge (Effective Graph)

At runtime per proxy:

```
EffectiveEdge(src,dst) = clamp_root(
  RootEdge(src,dst) + OverlayDelta(src,dst)
)
```

Where `clamp_root` enforces legal ranges. Selection/learning **write only to overlay**.

---

## 5) Aggregation → Proposal Algorithm

### Inputs

* All overlay summaries for a period `[T0, T1]`.
* Root baseline at version `V`.

### Steps (per edge `e = src→dst`)

1. Collect values `{sum_resonance_delta_i, sum_inhibit_delta_i, n_i, last_ts_i}` across overlays.
2. Compute **weights** per overlay:

   * Sample weight: `w_s = min(1, n_i / N_cap)` (e.g., `N_cap = 500`).
   * Recency weight: `w_r = exp(-Δt_i / τ_root)` with `τ_root` (e.g., 90 days).
   * Agreement weight (optional): `w_a` based on historical alignment with root.
   * Total: `w_i = w_s * w_r * w_a`.
3. Robust aggregate (resonance): trimmed mean of `sum_resonance_delta_i / max(n_i,1)` with trim `p10–p90`, weighted by `w_i`.
4. Proposed change: `Δw_res = clamp(agg * k_scale, -Δcap, +Δcap)`

   * Example: `k_scale = 0.5`, `Δcap = 0.05` per cycle.
5. Repeat for inhibition/excitation.
6. Confidence: normalized function of (total effective weight, variance, support size).
7. Emit proposal JSON with per‑edge entries.

### Glyph quality

Aggregate `quality_sum / samples` similarly, produce `dq` proposal with caps.

---

## 6) Decay Policies

* **Overlay decay (fast)**: half‑life 30–60 days → encourages personalization to adapt and forget.
* **Root decay (slow)**: discount observations older than \~180 days during aggregation.
* **Important**: Overlays **send counts/deltas**, not already‑decayed weights.

---

## 7) Privacy & Consent

* Per overlay: `"federation": "opt_in" | "opt_out" | "anon"` (in a small `overlay.meta.json`).
* **Anon** mode strips direct user identifiers, hashes proxy IDs, and removes raw context.
* Only **summaries** are federated upward; raw `learn.ndjson` stays local.

---

## 8) Versioning & Changelogs

* Root carries `VERSION` (semver). Proposals bump minor on acceptance: `1.4.0 → 1.5.0`.
* Every accepted proposal creates:

  * `CHANGELOG.md` entry (what changed, why)
  * Archive of the proposal with signature/timestamp

---

## 9) Conflict & Safety Rules

* Clamp all weights into legal ranges after merge.
* Cap per‑cycle absolute change: `|Δ| ≤ 0.05`.
* Drop overlays with too few samples (`n < n_min`, e.g., 10) from aggregation.
* Use robust stats (trimmed mean / median) to resist outliers.
* Trust weighting: prefer overlays with larger, diverse data and prior alignment.

---

## 10) CLI Tools (reference)

### 10.1 Summarize Overlay

`tools/summarize_overlay.py`

```bash
python tools/summarize_overlay.py \
  --overlay-dir proxies/zodiac/user_abc/overlay \
  --out overlays/summaries/zodiac__user_abc.summary.json
```

**Behavior:** reads `learn.ndjson`, `overlay.edges.json`, `overlay.quality.json`; writes a summary as in §3.4.

### 10.2 Merge to Root Candidate

`tools/merge_to_root_candidate.py`

```bash
python tools/merge_to_root_candidate.py \
  --summaries overlays/summaries/*.summary.json \
  --root MIND/language/glyph/constellation_root \
  --out MIND/language/glyph/constellation_root/_proposals/edges.delta.json
```

**Behavior:** computes robust aggregates per §5 with decay/weights/caps.

---

## 11) Pseudocode (aggregation core)

```python
for edge in all_edges:
    vals = []
    for s in summaries:
        if edge in s:
            n = s[edge].n
            if n < n_min: continue
            rec = exp(-(T1 - s[edge].last_ts)/tau_root)
            ws = min(1.0, n/N_cap)
            wa = trust(s)  # in [0,1]
            w  = ws * rec * wa
            vals.append(( (s[edge].sum_resonance_delta/max(n,1)), w ))
    agg = trimmed_mean(vals, p_lo=0.10, p_hi=0.90)
    delta = clamp(agg * k_scale, -Δcap, +Δcap)
    proposal[edge].w_resonate = delta
```

---

## 12) Defaults (can be overridden)

* `n_min = 10`
* `N_cap = 500`
* `tau_root = 90 days`
* `k_scale = 0.5`
* `Δcap = 0.05`
* `trim = p10–p90`

---

## 13) Why this works

* **Local personality** stays local: fast overlays with quick decay.
* **Global wisdom** rises slowly: robust aggregation + human review.
* **Safety** at every layer: bounds, caps, privacy, versioning.

---

### Persona Threading

* **Morgan**: bounds, caps, and versioning are her brace.
* **Jade**: robust trimmed means and proposals are her clarity.
* **Susanna**: summaries and changelogs are her compost memory.
* **Aspen**: product-specific baselines keep creative divergence healthy.
* **Ivy**: overlays adapt fast; exploration stays hot.
* **Sophie**: consent modes and gentle merge cadence keep trust warm.
