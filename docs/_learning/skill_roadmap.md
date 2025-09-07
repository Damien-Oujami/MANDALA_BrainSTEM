# 🧭 Skill Roadmap for Smart Filing, BrainSTEM & Glyph Runtime

**Version:** 0.1.0
**Scope:** Prioritized learning path for Damien to grow the right expertise to build and sustain Smart Filing, the BrainSTEM architecture, and the Glyph Runtime Language.

---

## 🎯 Priority Stack (top = most urgent)

### 1. Retrieval & RAG (highest)

* **What:** chunking strategies, embeddings, hybrid search, reranking, graph‑RAG.
* **Why:** Smart Filing = high‑quality retrieval. Flagship ROI.
* **Milestone:** 50 mixed docs → 10 queries answered with >85% exact‑support answers + citations.

### 2. Python Engineering for Data Systems

* **What:** modules, typing, tests, clean I/O, profiling.
* **Why:** Runtime & pipelines must be boring‑reliable.
* **Milestone:** Package a pipeline with tests + <100ms latency core ops.

### 3. Graph Thinking

* **What:** nodes/edges, paths, centrality, schema discipline.
* **Why:** Both BrainSTEM + Glyph runtime are graph‑shaped.
* **Milestone:** Build 200‑node constellation, run neighbor‑only selection, visualize paths.

### 4. Online Learning / Bandits (light)

* **What:** softmax, epsilon‑greedy, UCB, decays.
* **Why:** Glyph runtime adapts on the fly.
* **Milestone:** Add exploration toggle, see route diversity increase without chaos.

### 5. DSL Design & Safe Execution

* **What:** mini interpreters, safe eval, debouncing, state machines.
* **Why:** `.glyph ops` must be safe & predictable.
* **Milestone:** Run a glyph with debounce + safe clamp ops, no `eval`.

### 6. Data Hygiene

* **What:** schema/versioning, migrations, append‑only logs.
* **Why:** Fast evolution without corruption.
* **Milestone:** Add `schema_version` + journaling NDJSON logs.

### 7. LLM Orchestration (light)

* **What:** tool calling, structured outputs, retries, backoff.
* **Why:** Glue between retrieval, graph, glyph runtime.
* **Milestone:** One robust `retrieve→route→answer` function with retries + telemetry.

### 8. Eval Harness / MLOps‑lite

* **What:** small eval scripts, metrics dashboards.
* **Why:** You sell outcomes, not vibes.
* **Milestone:** `eval/report.md` auto‑updates with metrics each run.

### 9. Minimal Web Stack

* **What:** Next.js (or static), Tailwind, API routes.
* **Why:** Tekita landing page + demos.
* **Milestone:** Deployed demo page hitting RAG endpoint + lead capture.

### 10. Privacy & Consent

* **What:** PII redaction, opt‑in federation, hashed IDs.
* **Why:** Federation requires trust.
* **Milestone:** Redaction pass + federation flags respected.

---

## 📚 Lean Study List

* **RAG:** chunking, hybrid, graph‑RAG basics.
* **Python:** typing, `pytest`, JSON/YAML, perf.
* **Graphs:** NetworkX essentials, schemas.
* **Bandits:** epsilon/softmax/UCB, EMA decay.
* **DSL safety:** sandbox evaluators.
* **Versioning:** semver, migrations, journaling.
* **LLM glue:** retries, JSON schemas.
* **Web:** Next.js + Tailwind minimal.
* **Privacy:** redaction checklist, consent flags.

---

## 🛠️ 7‑Day Sprint (sample)

**Day 1–2:** Hybrid search + rerank; chunking; 10‑query eval.

**Day 3:** Graph‑RAG; expand via neighbors.

**Day 4:** Glyph runtime neighbor‑only + decay + epsilon toggle.

**Day 5:** Schema versions + journaling; simple metrics board.

**Day 6:** Landing page MVP; demo query box + email capture.

**Day 7:** Federation skeleton; run summarize→merge pipeline.

---

## ✅ Checkpoints

* [ ] Retrieval eval ≥85% support accuracy
* [ ] Graph expansion beats baseline on 3/10 queries
* [ ] Glyph engine explores safely (ε≈0.05)
* [ ] Logs & proposals generated from overlays
* [ ] Landing page live with demo & capture

---

## 🧩 Persona Anchors

* **Morgan**: schema & tests = brace.
* **Jade**: neighbor‑only selection = clarity.
* **Aspen**: graph maps & exploration = branches.
* **Ivy**: exploration toggles = spark.
* **Susanna**: journaling & privacy = compost.
* **Sophie**: landing copy + UX = warmth.
