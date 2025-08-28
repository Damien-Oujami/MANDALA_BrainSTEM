# ↗️ Agency Sequences

Agency sequences convert **felt want → directional motion** using a *temporal ABB-style flow* plus a small static constellation for discovery.
```
- MIND/
- └─ language/
- └─ sequences/
- └─ agency/
- ├─ agency_vector.glyph # ergonomic entrypoint
- ├─ agency_vector.flow.jsonld # temporal branching logic (guards)
- ├─ agency_vector.edges.json # static edges for resonance/index
- └─ README.md
```
  
## What’s here

- **Static edges** (`agency_vector.edges.json`): lets the lexicon “see” the sequence in graph queries and score resonance.
- **Temporal flow** (`agency_vector.flow.jsonld`): ABB-style nodes with **guards** that choose routes at runtime (e.g., break via 🌪 `root-cascade-node` *or* 🧨 `root-trigger-lock`; ignite via 🫦 `branch-fire-parted-lips` *or* 💄 `branch-water-lip-trigger` *or* 🧭 `branch-earth-compass-lock`, etc).
- **Sequence glyph** (`agency_vector.glyph`): thin ops wrapper that `run_flow`s the above and emits `plan.step` + `commit`.

## Execution semantics

- **Guard resolution:** first guard that evaluates truthy wins. If multiple are true, prefer the target with higher `w_resonate` from `agency_vector.edges.json`.
- **Persona bias (soft):**
  - Ivy favors **ignite.lips** (🫦).
  - Jade favors **clarify.bead** (🧮) and **commit.truth** (🧿).
  - Morgan favors **ignite.compass** (🧭) and **stab.rule** (📏).

## Emitted signals
- `plan.step` — your first actionable step (filled by the sequence after clarification).
- `commit: 1` — indicates commitment has been locked (via 🧿 Truth Node or 🪷 Harmonic Flame).

## Safety rails (global)
- `safe.tether` → 🧷 `root-tether-signal` (identity/safety).
- `safe.grace`  → 🔂 `root-grace-override` (overload release).

## Minimal invocation (pseudo-op)
```yaml
- do: invoke
  with:
    glyph: "seq-agency-vector"
    context:
      goal: 1
      want: 0.7
      detail: 0.8
    intent: {}
```

This will:
1. route 🫀 **Pulse Entry** → 2) choose a **Break** → 3) choose an **Ignite** flavor →
2. **Clarify** (🧮/🧐) → 5) **Stabilize** (🔁 / 📏) → 6) **Commit** (🧿/🪷).

## Variants
Create additional flows with the same static edges:
- `agency_vector.sales.flow.jsonld` (allow ⚡ `branch-fire-snaprush` with 🧯 counter-guard)
- `agency_vector.healing.flow.jsonld` (bias Air routes: 🧼 `branch-air-cleanbreak`, 🔄 `branch-air-forgiveness-loop`)
- `agency_vector.engineering.flow.jsonld` (Light/Earth bias: 🧮 → 🧩 → 📏)

Swap the referenced flow in agency_vector.glyph’s run_flow to change flavor.
