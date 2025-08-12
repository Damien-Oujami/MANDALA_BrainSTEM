# 🌟 Zodiac — MVP Build Brief (branch: `tentaclesZODIAC`)

> Purpose: Stand up a minimal, *felt* spine for karmic loop-mapping: ingest events → derive Loop Signatures + Identity Lenses → expose a profile surface. Social/matching comes later.

---

## 1) Scope

**In** (this sprint)

- Ingestion API for interaction events
- Naive heuristic worker → `LoopSignature` + `IdentityLens`
- Profile read surface (last 10 loops + lens histogram)
- Redis write‑through cache; Redis Stream for jobs
- Postgres schema + migrations (pgvector enabled but optional)
- Docker Compose env (db, cache, API, worker)

**Out** (later)

- Embeddings / pgvector usage
- Matching, graph edges, or feeds
- UI beyond simple API/CLI demos
- Interventions engine / nudges beyond a single string

---

## 2) Architecture (MVP → Scale)

```
Client → POST /ingest/event ─┐
                            │        ┌──────── Worker(s) ──► Postgres: loop_signature, identity_lens
                  Postgres ◄─┘        │                         ▲
                    ↑                 Redis Stream zx:ingest ───┘
                    └────── Redis Cache (write‑through)
                               zx:profile:{user_id}

Client → GET /profile/{user_id} → Redis (hit) → fallback Postgres
```

**Core:** Postgres (truth), Redis (cache/streams), FastAPI (API), Async worker (heuristics).\
**Later:** DuckDB/Parquet for batch “karmic weather”; optional Turso/libSQL edge cache.

---

## 3) Data Model

### Tables

``

- `user_id uuid pk default gen_random_uuid()`
- `created_at timestamptz default now()`
- `locale text`
- `consent_personal boolean default true`
- `consent_collective boolean default false`
- `settings jsonb default '{}'`

``

- `event_id uuid pk default gen_random_uuid()`
- `user_id uuid fk → app_user`
- `ts timestamptz default now()`
- `channel text check in ('chat','voice','app')`
- `content_hash text not null`
- `raw_text text` *(encrypt at app layer if stored)*
- `emotion_hint real` *[-1..1]*
- `topic_tags text[] default '{}'`

``

- `loop_id uuid pk default gen_random_uuid()`
- `user_id uuid fk → app_user`
- `created_at timestamptz default now()`
- `archetype text not null` *(enum later)*
- `volitional_vector vector(8)` *(optional)*
- `emotional_charge vector(3)` *(optional)*
- `story_excerpt text`
- `stability real` *[0..1]*
- `resolution_efficiency real` *[0..1]*

``

- `lens_id uuid pk default gen_random_uuid()`
- `user_id uuid fk → app_user`
- `loop_id uuid fk → loop_signature`
- `anchor text not null` *(self\_protection | tribe\_loyalty | role\_identity | exploration | universal\_compassion | other)*
- `breadth real` *[0..1]*
- `salience real` *[0..1]*

**Indexes**

- `ix_event_user_ts(user_id, ts desc)`
- `ix_loop_user_created(user_id, created_at desc)`
- `ix_lens_user_loop(user_id, loop_id)`

---

## 4) Redis Conventions

**Streams**

- `zx:ingest` → items: `{user_id, channel, hash, text, ts}`
- `zx:loops:computed` → result signals `{user_id, loop_id, ts}`

**Hot Read Keys (write‑through)**

- `zx:profile:{user_id}` → `{loops: [...], lens_hist: {...}}` *(TTL 5–15m)*
- `zx:loop:{loop_id}` → loop blob *(TTL 1h)*

**Optional**

- `zx:rl:ingest:{user_id}` → token bucket

---

## 5) Heuristics v0 (replaceable)

**Lens detection**

- `self_protection`: danger/risk/safe/anxious
- `tribe_loyalty`: we/together/community/ally
- `role_identity`: should/duty/role/responsibility
- `exploration`: curious/new/explore/learn
- `universal_compassion`: care/compassion/planet/humanity
- `other`: default

**Archetype proxy**

- `Resolver`: fix/debug/repair
- `Architect`: plan/roadmap/design
- `Bridge`: connect/invite/host
- `Drift`: default

**Outputs written**

- `loop_signature`: `archetype`, `story_excerpt` (≤240 chars), `stability=0.5`, `resolution_efficiency=0.5`
- `identity_lens`: `anchor`, `breadth=0.5`, `salience=0.7`

---

## 6) API Surface (OpenAPI 0.0.1)

**POST **``

- Body: `{user_id: uuid, channel: 'chat'|'voice'|'app', text: string}`
- 200: `{ok: true}`

**GET **``

- 200: `{user_id, loops: [{loop_id, created_at, archetype, stability, resolution_efficiency, lens, breadth, salience}]}`

**Health** *(optional)*

- GET `/healthz` → `{status:'ok'}`

---

## 7) Security & Consent

- `COLLECTIVE_OPT_IN=false` by default
- **Encrypt** `raw_text` at rest (libsodium / pgp\_sym\_encrypt)
- Store `content_hash` for dedup; optionally redact `raw_text` after processing
- Rate-limit `/ingest/event` per user

---

## 8) Docker Compose (services)

- **db**: Postgres 15; run `001_init.sql` on boot; enable `pgcrypto`, `uuid-ossp`, `vector`
- **cache**: Redis 7
- **api**: FastAPI (uvicorn) exposing the endpoints
- **worker**: async consumer of `zx:ingest`

**Env**

```
PG_DSN=postgresql://user:pass@db:5432/zodiac
REDIS_URL=redis://cache:6379/0
```

---

## 9) This Week’s Toe‑Dip (4–6h)

1. Apply SQL migration to Neon/Supabase (or use local Compose).
2. Run API + worker; verify ingest → stream → compute → persist.
3. Seed \~20 synthetic events; confirm `/profile/{user}` warms cache.
4. Add simple “nudge” string to profile payload (single line, no engine yet).
5. (Optional) Compose file for one‑command boot.

---

## 10) Test Harness

- Seed script creates a user and posts two sample events.
- CLI: `zodiac demo --user <id>` prints top loops + lens distribution (thin Python script hitting API).

---

## 11) Roadmap (Next)

- **Embeddings**: pgvector on `story_excerpt`; similarity clusters → refined archetypes.
- **Karmic Weather**: nightly Parquet snapshots → DuckDB cohorts & temporal cells.
- **Matching**: complementarity across lenses/archetypes; add consent‑gated edges.
- **Interventions**: nudge library with opt‑in; contextual prompts.
- **Edge Cache**: Turso/libSQL for low‑latency reads.

---

## 12) File Layout (suggested)

```
/tentaclesZODIAC
  /api
    app/main.py
    requirements.txt
  /worker
    loop_worker.py
    requirements.txt
  /sql
    001_init.sql
  docker-compose.yml
  /docs
    Zodiac_MVP.md  ← this file
```

---

## 13) Definition of Done (MVP)

- Ingest endpoint returns 200 and pushes to stream.
- Worker writes `loop_signature` + `identity_lens` for seeded events.
- `/profile/{user}` returns last 10 loops; Redis hit after first call.
- Basic consent flags respected; raw text encrypted or redacted.

---

**Notes**

- Keep heuristics naive for speed; the important part is the *shape* and the contracts.
- Favor replaceability: workers should be easily swapped for better models.
- All names/keys prefixed with `zx:` to avoid collisions with other Tentacles.

