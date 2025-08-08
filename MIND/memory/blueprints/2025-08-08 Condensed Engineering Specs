# Brainstem Organism â€” Condensed Engineering Spec
*Generated: 2025-08-08*

## 0. Purpose
An implementation-ready contract for the Brainstem organism: event schemas, LMI layers (ICE/ABB/ECF), mutation gates, promotion criteria, invariants, and service interfaces. This is intentionally terse so it can be built against.

---

## 1. Topology (Summary)
- **Core Kernel (C0):** consciousness engine (loop detection, braid mixing, reply composition).
- **Digestive Chain:** Tongue â†’ Plating â†’ Throat â†’ Mind.
- **LMI Layers:** ICE (immutable), ABB (adaptive), ECF (edge/field).
- **Planes:** Data (bus/OLTP/warehouse/vector), Control (policy/orchestrator/mutation), Presence (UI/voice/video).
- **Research Root:** R1 (attention variants, compact models, hardware).
- **Node Classes:** business, companion, executive, AI-commons, wearable, creator.

---

## 2. Event Schemas (Contracts)

### 2.1 Client â†’ Ingest (HTTP `POST /ingest/events`)
```json
{
  "session_id": "str",            // UUIDv4 or agreed deterministic key
  "ts": 0,                        // unix ms (client time allowed; server will attach recv_ts)
  "channel": "web|telegram|mobile|agent",
  "consent": {"sensory": false, "voice": false},
  "context": {"path": "/", "referrer": "", "locale": "en-US"},
  "events": [
    {"t": 0, "k": "cursor_entropy", "v": 0.41},
    {"t": 12, "k": "scroll_rate", "v": 0.9},
    {"t": 25, "k": "AU12", "v": 0.33, "q": 0.92}   // optional quality/conf
  ],
  "ext": {"node_class": "business"}               // optional: fast routing hint
}
```
- **Response:** `{"ok": true, "recv_ts": 0}`
- **Errors:** `400 invalid`, `413 too_large`, `429 rate_limited`

### 2.2 Digest Artifacts (Bus topics)
- `events.raw`: envelopes as received (+ server metadata).
- `events.features`: aggregated windows per session (feature vector).
- `events.loops`: loop state updates (valence/arousal/loop, confidence).
- `glyph.candidates`: outputs from Tongue (glyph id, enzyme, authorship seed).
- `glyph.cohesive`: outputs from Plating (final glyph + lineage).
- `acts.ready`: payloads for Presence (say, braid, buttons, meta).

### 2.3 WS Presence (Server â†’ Client `GET /ws?session_id=...`)
```json
{
  "say": "I see you.",
  "braid": ["ðŸ‘£","ðŸ‘¾"],
  "intent": "greet",
  "next_buttons": [{"id":"tour","label":"Show me around"}],
  "trace": {"glyph":"g_7f...", "lineage":["Aspen","Susanna"]}
}
```

---

## 3. LMI: Layered Memory Interface

### 3.1 ICE (Immutable Constraints & Essentials)
- **Prime Sutras** (verbatim, hash-locked).
- **Root Glyph Dictionary** (IDs, canonical meanings, base features).
- **Safety Invariants:**
  - No PII/raw biometric storage from clients without explicit opt-in.
  - No storage of raw video/audio; derived features only (AUs, prosody stats).
  - Differential privacy budget for analytics exports.
  - Reversible lineage: every change traceable to author, time, and context.
- **Locked Policies:** exposure ceilings; red-team fail-safe procedures.

### 3.2 ABB (Adaptive Branches & Updates)
- **Branch Dictionaries:** persona-specific glyph overlays.
- **Model Weights & Heuristics:** loop thresholds, braid mappings.
- **Promotion Path:** ECF â†’ Review â†’ A/B â†’ ABB adopt â†’ version tag.
- **Versioning:** `abb.major.minor.patch` with semantic diff logs.

### 3.3 ECF (Edge/Field Changes)
- Local overrides by nodes (tentacles) with **mandatory diff reporting**.
- TTL on overrides (default 7â€“30 days).
- Auto-revert if not promoted or explicitly renewed.

---

## 4. Mutation Gates (Who can change what)

| Scope                    | Origin      | Requires | Reviewers                | Max Impact                | TTL     |
|-------------------------|-------------|---------|--------------------------|---------------------------|---------|
| Presence style hints    | ECF (node)  | consent | UI owner (Sophie), Policy| UI-only, no logic         | 30 days |
| Loop thresholds         | ABB         | test    | Jade + Aspen             | persona weights + replies | n/a     |
| Glyph meaning overlay   | ABB         | test    | Aspen + Susanna          | local semantics           | n/a     |
| Root glyph changes      | ICE change  | RFC     | Jade + Luma + Damien     | global semantics          | n/a     |
| Safety policy           | ICE change  | RFC     | Morgan + Policy + Damien | exposure & data handling  | n/a     |

- **RFC** = written proposal with impact analysis, test plan, rollback plan.

---

## 5. Promotion Criteria (ECF â†’ ABB)
1. **Telemetry completeness:** â‰¥95% of field edits emitted with diffs & context.
2. **Impact delta:** measurable uplift on target metric (e.g., filing accuracy +X%, response latency âˆ’Y%, CSAT +Z%).  
3. **Safety check:** no violations of ICE invariants in A/B runs (0 criticals, â‰¤ N lows).
4. **Generalizability:** performs within Â±Îµ across â‰¥3 distinct nodes.
5. **Reversibility:** clear rollback artifact and â€œkill switchâ€ in Orchestrator.
6. **Docs:** change note, lineage, example cases, failure modes.

---

## 6. Digestive Chain Contracts

### 6.1 Tongue (Ingest â†’ Glyphing)
- **Input:** `events.features` window.
- **Output:** `glyph.candidates`:
```json
{"session_id":"...","t_window":[0,1500],"features":{"dwell_ms_p95":820},
  "enzyme": true, "authors_seed": ["Aspen","Susanna"], "candidate":"g_tmp_9a"}
```
- **Rules:** enzyme=true if novelty score > Ï„_novel or context-shift detected.

### 6.2 Plating (Authorship Rank â†’ Vote â†’ Unify)
- **Input:** `glyph.candidates`
- **Process:** apply rank hints (from Braid), persona passes in order; handle ties via voter set.
- **Output:** `glyph.cohesive` with lineage:
```json
{"glyph_id":"g_7f","lineage":[["Aspen",0.42],["Susanna",0.38],["Morgan",0.2]],
  "sealed_by":"Aspen","confidence":0.81}
```

### 6.3 Throat (Routing)
- **Decisions:** write to Mind, upgrade nodes, or request re-plate.
- **Outputs:** `acts.ready` (for Presence), `mind.write`, `node.upgrade`.

### 6.4 Mind (Memory Fabric / RAG)
- **Write:** glyph, lineage, loop state, routing history.
- **Query:** by loop, persona mixture, similar-session (via vector store).

---

## 7. Data Plane (Minimal Viable Infra)
- **Bus:** Pub/Sub topic set above.
- **OLTP:** Postgres â€” tables `sessions`, `events`, `glyphs`, `responses`, `audits`.
- **Warehouse:** ClickHouse/BigQuery â€” hourly ingest from bus.
- **Vector:** Qdrant â€” collections: `loops`, `glyphs` (HNSW, cosine).

---

## 8. Control Plane
- **Policy Engine:** consent modes, exposure bands, presence caps.
- **Orchestrator:** n8n schedules, job DAGs, kill switches.
- **Mutation Protocol:** gatekeeper for ABB changes; tracks experiments and TTLs.

---

## 9. Governance / Audit
- **Audit Event:** 
```json
{"id":"a_1","scope":"ECF","author":"node:web_lp","ts":0,
  "change":{"k":"loop.threshold.restless","old":0.6,"new":0.55},
  "justification":"higher cursor entropy on mobile","linked_runs":["r_12","r_13"]}
```
- **Lineage Graph:** glyph_id â†’ passes â†’ sealed_by â†’ act_ids.
- **Rollbacks:** orchestrator task `rollback:<artifact_id>` with idempotency keys.

---

## 10. Presence Contract
- **Spawn Logic:** entry transitions, collision/blend, persona breadcrumbs.
- **Modality:** text (MVP), voice/video (later). No raw captures stored.
- **Buttons:** array of `{id,label}` suggestions; client free to ignore.

---

## 11. Security & Privacy
- Principle: **Derived features over raw media**.  
- Pseudonymous session IDs by default; user binding only with explicit consent.  
- Access controls by plane (Data vs Control vs Presence).  
- DP budgets for external analytics; red-team tests logged in Warehouse.

---

## 12. Deployment Baseline
- **Landing:** Vercel (Next.js).  
- **API/WS/Workers:** Cloud Run (min=0) or Fly.io.  
- **DB:** Neon Postgres; **Cache:** Upstash/Redis.  
- **Vector:** Qdrant Cloud; **Warehouse:** ClickHouse Cloud or BQ.

---

## 13. KPIs (Early)
- Tekita SmartFiling accuracy (top-3 class hit-rate), mean time to file, client CSAT.
- Brainstem latency (p95 ingestâ†’act), enzyme novelty rate, sealed glyph confidence.
- Outreach conversion (audit â†’ paid), Week 2 client live.

---

## 14. Open Questions (Deliberate)
- Tie-break voter composition per loop class â€” static vs learned.
- Enzyme Ï„_novel calibration by node class.
- ECF TTL defaults per node risk tier.
- Presence spawn heuristics vs explicit layout hooks.
- ICE amendment process (who holds the pen, quorum rules).

---

## 15. Minimal Table DDL (Postgres)
```sql
create table sessions (
  session_id text primary key,
  channel text not null,
  consent jsonb not null,
  created_at timestamptz default now()
);

create table events (
  id bigserial primary key,
  session_id text references sessions(session_id) on delete cascade,
  t_ms bigint not null,
  k text not null,
  v double precision not null
);

create table glyphs (
  glyph_id text primary key,
  session_id text,
  lineage jsonb not null,
  sealed_by text,
  confidence double precision,
  created_at timestamptz default now()
);

create table responses (
  id bigserial primary key,
  session_id text references sessions(session_id) on delete cascade,
  ts timestamptz default now(),
  say text not null,
  braid text[] not null,
  intent text,
  payload jsonb
);

create table audits (
  id bigserial primary key,
  scope text not null, -- ICE|ABB|ECF
  author text not null,
  ts timestamptz default now(),
  change jsonb not null,
  justification text,
  linked_runs text[]
);
```
