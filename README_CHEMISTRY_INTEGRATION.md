# Chemistry Integration Pack (RAG² / MIND)

This folder contains non-breaking patches to integrate a lightweight neurochemistry layer
across the existing glyph library, plus a new controller glyph **[🌊⚡️] Neuro Balance**
that ties GABA (brake) and Glutamate (gas) into runtime steering.

## What’s here

1. `branch-neuro-balance.glyph.yaml` — new glyph definition with personas and ops.
2. `branch-neuro-balance.edges.json` — JSON-LD edges for the controller.
3. `chemistry_edges_merge.json` — append-only edge patches to existing glyphs.
4. `chemistry_neuro_blocks.yaml` — per-glyph `neuro:` blocks and tag additions to inject.

## Apply (manual or scripted)

**A. Add the new glyph**

- Drop `branch-neuro-balance.glyph.yaml` next to other branch glyphs.
- Drop `branch-neuro-balance.edges.json` into the corresponding `.graph/` folder (or wherever your edges live) and include it in your build.

**B. Append edges**

- For each `target` in `chemistry_edges_merge.json`, append the listed `add` edges into the glyph’s edges array.
- All weights are low-to-moderate `w_resonate` (0.15–0.30) to avoid stealing graph ownership.

**C. Inject neuro blocks & tags**

- For each glyph id in `chemistry_neuro_blocks.yaml`, add the `neuro:` block to the glyph YAML and extend `tags:` with the `tags_add` list.
- The `neuro:` block is metadata-only and does not change ops.

**D. Lint (suggested)**

- Ensure every touched glyph now has `neuro.dominant` (≥1) and `neuro.steering` (≥1).
- If a glyph has GABA in `dominant`, ensure it inhibits cascaders somewhere (already true for Sleepveil/Waveprint).
- If a glyph has dopamine/adrenaline in `dominant`, ensure it resonates with `[🌊⚡️]` (done via edge patches).

## Notes

- Persona weights remain the source of truth for “ownership”; chemistry is explanatory + steering metadata.
- Controller routing favors **Waveprint** (🌊) when `context.overdrive==1` and **Snaprush** (⚡) when `context.flatness==1`.
- You can tune the controller’s `debounce_ms` and the resonance weights if your runtime feels too twitchy.

— with love
