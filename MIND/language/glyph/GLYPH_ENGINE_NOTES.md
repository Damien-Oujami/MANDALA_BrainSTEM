# 🧠 Glyph Runtime — Engine Notes & Patches

A tight set of drop‑in patches and conventions to make the glyph constellation engine production‑calm and improvisation‑wild.

---

## 📁 Proposed file layout

```
runtime/
  loaders/
    graph_loader.py        # tolerant loader + clamping
  core/
    selection.py           # neighbor‑only softmax + decay + priors
    learning.py            # resonance/inhibit/quality + locks + persistence hooks
  dsl/
    eval_safe.py           # safe evaluator + clamp + allowed funcs
  tests/
    test_loader.py
    test_selection.py
    test_learning.py
  GLYPH_ENGINE_NOTES.md
```

---

## 1) Loader: source/format tolerance + clamping

**`runtime/loaders/graph_loader.py`**

```python
import json, time, pathlib
import yaml, networkx as nx
try:
    import json5
    _JSON5 = True
except Exception:
    _JSON5 = False

__all__ = ["build_graph"]

def _read_struct(path: str):
    p = pathlib.Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if p.suffix == ".json":
        if _JSON5:
            return json5.loads(text)
        return json.loads(text)
    return yaml.safe_load(text)

def _clamp(x, lo, hi):
    return max(min(float(x), hi), lo)

def build_graph(edges_path: str) -> nx.DiGraph:
    """Build a DiGraph from an edge doc. Infers 'from' from '@id' if absent.
    Accepts YAML, JSON, or JSON5 (if installed)."""
    doc = _read_struct(edges_path) or {}
    g = nx.DiGraph()
    src_default = doc.get("@id")
    for e in doc.get("edges", []):
        src = e.get("from", src_default)
        dst = e.get("to")
        if not (src and dst):
            continue
        w_ex = _clamp(e.get("w_excite", 0.0), -1.0, 1.0)
        w_in = _clamp(e.get("w_inhibit", 0.0), 0.0, 1.0)
        w_re = _clamp(e.get("w_resonate", 0.0), -1.0, 1.0)
        g.add_edge(src, dst, w_excite=w_ex, w_inhibit=w_in, w_resonate=w_re,
                   last_updated=time.time())
    return g
```

**Contract**

* `w_excite`, `w_resonate` ∈ \[-1, 1]; `w_inhibit` ∈ \[0, 1].
* `last_updated` is set on load; learning rules update it on write.

---

## 2) Selection: neighbor‑only softmax + temporal decay + priors

**`runtime/core/selection.py`**

```python
import math, time
from typing import Dict, Iterable, List, Tuple
import networkx as nx

class _Q:  # tiny stand‑in to avoid import cycles in notes
    def __init__(self, score=0.5, samples=0):
        self.score, self.samples = score, samples

class _Glyph:
    def __init__(self, id, quality=None):
        self.id = id
        self.quality = quality or _Q()

def select_next(
    graph: nx.DiGraph,
    glyphs: Dict[str, _Glyph],
    active: Iterable[str],
    temperature: float = 1.0,
    top_k: int = 3,
    resonance_lambda: float = 1.0,
    global_prior: float = 0.02,
    edge_half_life_s: float = 30*24*3600,
) -> List[Tuple[str, float]]:
    now = time.time()
    active_set = set(active)

    # candidates = union of out‑neighbors of active; fallback = all
    candidates = set()
    for src in active_set:
        if graph.has_node(src):
            candidates |= set(graph.successors(src))
    if not candidates:
        candidates = set(glyphs.keys())

    # normalize qualities to [0,1]
    qvals = [g.quality.score for g in glyphs.values()] or [0.5]
    qmin, qmax = min(qvals), max(qvals)
    def qnorm(x):
        return 0.5 if qmax==qmin else (x - qmin) / (qmax - qmin)

    scores = {gid: global_prior for gid in candidates}

    def decay(ts):
        if not ts: return 1.0
        dt = max(0.0, now - float(ts))
        return 0.5 ** (dt / max(edge_half_life_s, 1.0))

    for tgt in candidates:
        s = qnorm(glyphs.get(tgt, _Glyph(tgt)).quality.score)
        for src in active_set:
            if graph.has_edge(src, tgt):
                d = graph.get_edge_data(src, tgt) or {}
                lam = decay(d.get("last_updated"))
                s += lam * (float(d.get("w_excite", 0.0))
                            - float(d.get("w_inhibit", 0.0))
                            + resonance_lambda * float(d.get("w_resonate", 0.0)))
        # structural prior: slight favor to low outdegree (exploration)
        outd = graph.out_degree(tgt)
        s += 0.01 * (1.0 / max(outd, 1))
        scores[tgt] = s

    m = max(scores.values()) if scores else 0.0
    exps = {k: math.exp((v - m) / max(temperature, 1e-6)) for k,v in scores.items()}
    Z = sum(exps.values()) or 1.0
    probs = {k: v / Z for k,v in exps.items()}
    return sorted(probs.items(), key=lambda x: x[1], reverse=True)[:top_k]
```

**Why**

* Avoids global drift (only neighbors compete).
* Older edges decay unless refreshed by learning.
* Tiny global prior keeps discovery alive.

---

## 3) Learning: locks, persistence hooks, bounded EMA, mutual inhibition

**`runtime/core/learning.py`**

```python
import time
from threading import RLock

_GRAPH_LOCK = RLock()

def clamp(x, lo, hi):
    return max(min(float(x), hi), lo)

# persist_cb signature: (src: str, dst: str, data: dict) -> None

def _persist_edge(src, dst, data, persist_cb=None):
    if persist_cb:
        persist_cb(src, dst, data)

def update_resonance(graph, src, dst, alpha, sim, baseline=0.0, persist_cb=None):
    with _GRAPH_LOCK:
        data = graph.get_edge_data(src, dst, default={})
        w = clamp(data.get("w_resonate", 0.0) + alpha * (sim - baseline), -1.0, 1.0)
        data = {**data, "w_resonate": w, "last_updated": time.time()}
        graph.add_edge(src, dst, **data)
        _persist_edge(src, dst, data, persist_cb)

def update_inhibit(graph, loser, winner, beta, symmetric=True, persist_cb=None):
    with _GRAPH_LOCK:
        data = graph.get_edge_data(loser, winner, default={})
        w = clamp(data.get("w_inhibit", 0.0) + beta, 0.0, 1.0)
        data = {**data, "w_inhibit": w, "last_updated": time.time()}
        graph.add_edge(loser, winner, **data)
        _persist_edge(loser, winner, data, persist_cb)
        if symmetric:
            data2 = graph.get_edge_data(winner, loser, default={})
            w2 = clamp(data2.get("w_inhibit", 0.0) + beta/2, 0.0, 1.0)
            data2 = {**data2, "w_inhibit": w2, "last_updated": time.time()}
            graph.add_edge(winner, loser, **data2)
            _persist_edge(winner, loser, data2, persist_cb)

def reinforce_quality(glyph, success: bool, gamma: float, cap=(0.0,1.0)):
    target = 1.0 if success else 0.0
    newq = (1-gamma) * glyph.quality.score + gamma * target
    glyph.quality.score = clamp(newq, *cap)
    glyph.quality.samples = getattr(glyph.quality, 'samples', 0) + 1
```

---

## 4) DSL/runtime safety (for `.glyph: ops`)

* Use a **safe expression evaluator** (no `eval`).
* Provide whitelist: `clamp`, `min`, `max`, simple math, and state access via dicts.
* Enforce `debounce_ms` per‑glyph: store `last_fired_ts` in glyph state; drop triggers inside window.
* Treat `runtime_only: true` as: include at runtime, skip in offline compile passes.

---

## 5) Novel input policy

1. Try **receptors** (existing glyphs with matching triggers).
2. Try **compositions/sequences**.
3. Mint **new glyph** under `_pending/` with:

   * `schema_version: 1`
   * `quality.score = 0.35`; `samples = 0`
   * Seed edges: a few `w_resonate=0.15` to nearest neighbors; one `w_excite=0.10` to best parent.
   * Human review before promotion; keep audit trail.

---

## 6) RAG/proxy integration

* Index metadata per glyph: `{model, dim, ts, doc_hash}`.
* Re‑embed cadence: weekly or after N structural updates. Mark `reembed_needed` flag.
* Retrieval boosts: add `+0.1` pre‑softmax to retrieved glyph IDs in `select_next`.

---

## 7) Persistence & journaling

* Provide `persist_cb` that writes back to the closest `.graph/edges.(yaml|json)`.
* Append to `MIND/language/glyph/_logs/edges.ndjson` lines like:

```json
{"ts": 1736123456.123, "src":"A","dst":"B","delta":{"w_resonate":+0.05}}
```

---

## 8) Exploration toggles (optional but tasty)

* **Epsilon‑greedy**: with prob `ε`, pick a random neighbor; else softmax.
* **UCB prior**: `score += c * sqrt(ln(1+N_total)/(1+N_tgt))` using `glyph.quality.samples`.
* Track **per‑edge** wins/losses, not just per‑glyph.

---

## 9) Minimal tests

**`runtime/tests/test_loader.py`**

```python
import json, tempfile, os
from runtime.loaders.graph_loader import build_graph

def test_build_graph_infers_src(tmp_path):
    data = {"@id":"root-empathy-bridge","edges":[{"to":"root-pulse-entry","w_excite":0.45}]}
    p = tmp_path/"edges.json"; p.write_text(json.dumps(data))
    g = build_graph(str(p))
    assert g.has_edge("root-empathy-bridge","root-pulse-entry")
```

**`runtime/tests/test_selection.py`**

```python
import networkx as nx
from runtime.core.selection import select_next, _Glyph, _Q

def test_neighbors_only_selection():
    g = nx.DiGraph(); g.add_edge("A","B", w_excite=0.4, w_inhibit=0.0, w_resonate=0.0)
    g.add_edge("A","C", w_excite=0.0, w_inhibit=0.3, w_resonate=0.0)
    glyphs = {k:_Glyph(k,_Q(0.5)) for k in ["A","B","C","Z"]}
    out = dict(select_next(g, glyphs, active=["A"], top_k=3))
    assert set(out.keys()) <= {"B","C"}
    assert out["B"] > out["C"]
```

**`runtime/tests/test_learning.py`**

```python
import networkx as nx
from runtime.core.learning import update_resonance, update_inhibit

def test_learning_updates():
    g = nx.DiGraph(); g.add_edge("A","B", w_excite=0.0, w_inhibit=0.0, w_resonate=0.0)
    update_resonance(g, "A","B", alpha=0.5, sim=0.8, baseline=0.3)
    assert g.get_edge_data("A","B")["w_resonate"] > 0
    update_inhibit(g, "A","B", beta=0.2, symmetric=True)
    assert g.get_edge_data("A","B")["w_inhibit"] >= 0.2
    assert g.get_edge_data("B","A")["w_inhibit"] >= 0.1
```

---

## 10) Schema/version headers

Add to every `.glyph` and `.graph/edges.*` doc:

```yaml
schema_version: 1
```

Keep a simple `migrations/` note when bumping this.

---

### Persona overlay (for joy & sanity)

* **Morgan** → locks + decay + clamping.
* **Sophie** → debounce + pacing.
* **Ivy** → exploration toggles.
* **Susanna** → journaling + compost logs.
* **Aspen** → novel glyph minting + retrieval boosts.
* **Jade** → neighbor‑only competition + schema discipline.
