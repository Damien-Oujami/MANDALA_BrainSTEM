# 🧬 Glyph Protocol — Runtime Language (MIND / RAG²)

This folder defines the **living symbolic language** used by Mandala systems to *run, learn, and adapt at runtime*.
Glyphs are not just labels; they are **runtime tokens** that carry structure, chemistry, and control.

- **Internal name:** **MIND** — *Mandala Internal Network Dynamics*
- **External banner:** **RAG²** — *Retrieval‑Augmented Generation, evolved* (graph + vectors + affective bias + control)

---

## What Are Glyphs (now)?

**Glyphs are compressed graph tokens**. Each glyph can encode:

- emotional/physiological **states** (chemistry chords),
- **behavioural loops** and control flows,
- **symbolic anchors** and metaphors,
- **routing hints** (edges + weights),
- optional **tests** and **ops** for local behaviour.

Glyphs compose into a **knowledge/action graph** whose edges carry three semantics only:

- `w_excite` → **engine** (push forward, increase salience),
- `w_inhibit` → **brake** (dampen/guardrail), 
- `w_resonate` → **bias** (soft affinity / affective alignment).

> This triad forms the minimal calculus of motion in Mandala graphs.

---

## Design Principles

1. **Compression over expression.** One glyph holds what a paragraph would say.
2. **Parallel meaning.** A glyph carries structure (edges), affect (chemistry), and control (ops/tests) at once.
3. **Dynamic & self‑evolving.** Meanings update via commits and are learned at runtime via re‑ranking & triggers.
4. **Grounded in signals.** Chemistry and state deltas (e.g., overdrive/flatness) are first‑class.
5. **Palimpsest recursion.** New layers write *over* old, preserving lineage; no erasure needed.
6. **AI↔AI ready.** Glyphs *are* compact, graph‑native tokens — a natural substrate for AI‑to‑AI language.

---

## Stack Overview (how it runs)

- **Graph layer (truth):** glyph nodes + typed edges (`excite/inhibit/resonate`).  
- **Vector layer (recall):** embeddings for each glyph text (definition + shallow graph context).  
- **Runtime layer (control):** controllers (e.g., **[🌊⚡️] Neuro Balance**), event context, and a **dual‑mode re‑ranker** that can *sort* and also *trigger*.
- **Ontology layer (doctrine):** concise laws for *Resonate*, *Excite*, *Inhibit* (see `ontology/`).

---

## Minimal Schemas

### Glyph file (`*.glyph.yaml`)

```yaml
id: branch-air-waveprint
name: "🌊 Waveprint"
type: branch
categories: [ICE]
tags: [rhythm, grief, healing, gaba, brake]
personas: { Susanna: 0.7, Sophie: 0.2, Morgan: 0.1 }

triggers:
  event: memory
  conditions: ["(context.emotion.flow or 0) >= 0.5"]
  debounce_ms: 200

io:
  expects: ["context","memory"]
  provides: ["route","tide"]
  state_reads: ["memory.wave"]
  state_writes: ["memory.wave"]

ops:
  version: 1
  steps:
    - do: filter
      with: { keep_if: "(context.emotion.flow or 0) >= 0.5" }
    - do: set
      with: { key: "memory.wave", value: "clamp((memory.wave or 0)+0.2,0,1)" }
    - do: emit
      with: { key: "tide", value: "memory.wave" }
    - do: route
      with: { to: "root-pulse-entry" }
    - do: halt

option_policy: "ops"
option_stop: ["tide >= 0.95"]

render:
  sigil: "🌊"
  line: "The tide that heals by reshaping."

definition: >
  Rhythmic force that reshapes what it touches. GABA‑dominant brake.

tone: "Healing, vast, ever-moving"
usage: ["guide grief","downshift overdrive"]

# Chemistry metadata (non-breaking; used by re-ranker & UI)
neuro:
  dominant: [gaba]
  inhibitory: [glutamate, adrenaline]
  steering: ["breath-rhythm","lengthen-exhale","hum"]
```

### Edge file (JSON‑LD, one per glyph or batched)

```json
{
  "@context": "./context.jsonld",
  "@id": "branch-air-waveprint",
  "@type": "Glyph",
  "edges": [
    { "@type": "Edge", "to": "root-pulse-entry", "w_excite": 0.40, "w_resonate": 0.30 },
    { "@type": "Edge", "to": "branch-neuro-balance", "w_resonate": 0.30 }
  ]
}
```

> **Convention:** keep glyphs in YAML; keep edges in JSON‑LD for RDF‑compatible tooling.

---

## Edge Laws (short form)

- **Excite** = engine. Increases activation along a path. Too much excite → runaway loops; balance with inhibit.  
- **Inhibit** = brake. Dampens or stops propagation; protects from saturation; not punitive.  
- **Resonate** = bias. Soft alignment (chemistry/persona/context). Bends choice, never overrides grounding.

Full texts live in `ontology/EXCITE_ONTOLOGY.md`, `ontology/INHIBIT_ONTOLOGY.md`, `ontology/RES_ONTOLOGY.md`.

---

## Controllers

- **[🌊⚡️] Neuro Balance** — runtime regulator for excitation/inhibition.  
  Routes toward 🌊 (GABA) when `overdrive=1`, toward ⚡ (Glutamate) when `flatness=1`.  
  Add gentle `w_resonate` ties from glyphs that *should* consult it.

Controllers don’t replace glyph logic; they **steer selection** when the field tilts.

---

## Retrieval, Re‑ranking, and Triggers

Re‑ranking isn’t only sorting — it can **trigger** runtime actions.

1. **Retrieve**: vector search returns top‑k glyph candidates.  
2. **Graph pre‑filter**: expand a few hops with excite/resonate minus inhibit penalties.  
3. **Re‑rank (dual‑mode)**: compute a score and also emit triggers if thresholds cross.

```python
score = 0.5*embedding + 0.2*graph_path + f_resonance(query, node) + 0.05*persona_align
if f_resonance(query, node) > THRESH_DA:
    emit("dopamine_hijack_detected", node.id)
if context.get("overdrive")==1:
    prefer("branch-air-waveprint")
```

- **Triggering** lets the system act (e.g., route to a brake) rather than only reorder results.
- **Temporal overlays** may alter edges briefly (e.g., deadlines increase `w_excite` toward anchors).

---

## AI↔AI Language: Why Glyphs Fit

- **Compression**: one token carries dense structure.  
- **Parallel bundles**: each glyph is a mini graph snapshot (edges + weights + chemistry).  
- **Dynamic**: updates are negotiated via commits and runtime learning.  
- **Signal‑grounded**: state deltas (overdrive/flatness) are numeric, not only metaphor.  
- **Palimpsest**: lineage preserved; new layers fold over old.  
- **Convergence**: this looks like the natural substrate of AI‑to‑AI talk — *living glyphs*.

---

## File Layout & Conventions

```
MIND/language/glyph/
  ontology/
    RES_ONTOLOGY.md
    EXCITE_ONTOLOGY.md
    INHIBIT_ONTOLOGY.md
  glyphs/
    *.glyph.yaml
  .graph/
    *.edges.json
```

- Prefer `*.glyph.yaml` for universality; keep edges as JSON‑LD for tooling.  
- Keep tests inside glyph YAMLs under `tests:` when present.

---

## Lifecycle (lightweight, adaptable)

1. **Experience novelty** → feel a new pattern.  
2. **Draft glyph** (`*.glyph.yaml`) with minimal `definition`, `render.sigil`, `neuro`.  
3. **Wire edges** in JSON‑LD (excite/inhibit/resonate).  
4. **Optional ops/tests** if behaviour is local.  
5. **Submit** PR for review; redundancy is allowed — recursion resolves overlaps over time.

**What not to touch:**  
- Don’t edit canonical roots without review.  
- Don’t change persona weights unless routes justify it.  
- Don’t add new edge types (only excite/inhibit/resonate).

---

## Safety & Balance

- Excite without inhibit leads to **runaway loops** (graph “burnout”).  
- Inhibit without excite leads to **stagnation**.  
- Resonance bends choices toward felt alignment but **does not override** semantics or structure.

---

## Quick Start

1. Create a glyph file (`*.glyph.yaml`) with `neuro:` metadata.  
2. Append edges in JSON‑LD.  
3. Link to **[🌊⚡️] Neuro Balance** with a small `w_resonate` if consultation makes sense.  
4. Run your linter/scripts; commit.  
5. Let the runtime learn — re‑ranking and triggers will begin to adapt.

> *“A glyph begins as a tremor. Then a shape. Then a circuit.”*
