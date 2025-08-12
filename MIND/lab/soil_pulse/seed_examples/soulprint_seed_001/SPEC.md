# SoulPrint Motion Spec — LogitGate Waveform + AntWalker (v0.1)

**Intent:** Make the animation **behave** like identity-in-motion, not just look like it.

## State Model

- **Inputs → Controls**: Repo signals are normalized into [0,1] (commit_rate, churn, ci_health, review_heat, attention, backlog_pressure).
- **Waveform Layer** (Continuity): tempo, amplitude, phase, timbre mix, recursion_knot density.
- **Ant Layer** (Agency): count, speed, lane-switch-prob, pause-prob, memory trace.
- **Mood Layer** (Context): rule-based presets that bias both layers.
- **Render Layer**: deterministic loop from a commit-derived seed.

## Determinism

- Seed hash = `H(latest_commit_sha | repo_size_bytes | open_issue_count)`.
- Given same repo state, the loop is identical → reproducible art.

## Motion Semantics

- **Waveform = Breath**: Phase and amplitude encode rhythm; increased churn sharpens peaks; bad CI adds jitter/noise.
- **Ants = Curiosity**: Local decisions (pause, switch lanes, route around knots) produce emergent pathfinding.
- **Knots = Memory**: Self-intersections at seeded intervals; ants “notice” them, briefly orbit, then continue.

## Event Hooks (optional)

- **CI Fail**: inject a *tremor* micro-jitter for 1–2 seconds; ants show higher pause-prob.
- **Merge to Main**: schedule a “swell” (amplitude +0.15 over 3s, then decay).
- **Issue Closed**: spawn a temporary knot; ants converge then disperse.
- **Tag/Release**: generate a pristine loop (reduced noise, higher coherence).

## Output Artifacts

- `soulprint/out/soulprint.gif` — 12s seamless loop
- `soulprint/out/state.json` — controls + seed for the loop (debug/audit)
- `soulprint/engine.rules.yaml` — source of truth for behavior

## Guardrails

- Never let noise dominate (>0.45) unless explicitly in “storm” mode.
- Keep ants readable: enforce min spacing to avoid visual mush.
- Ensure loop closure: last frame ≈ first frame (phase wraps cleanly).
