# Operator Plan — Industry Coherence (v1)
**Date:** 2025-09-07

This plan operationalizes the *IndustryCoherence* ECF mode to move from **development → happy clients + BrainSTEM digesting**.

---

## 0) North Star
- **Product:** Enterprise Coherency Engine (Smart‑Filing + Resonant Graph + LAM signals).
- **Outcome:** Clients file/retrieve with high accuracy, explainable graph paths, and compliance snapshots; **all events** logged to BrainSTEM for continuous upgrades.

---

## 1) Scope (Jade — Delete)
**In‑scope**
- Smart‑Filing SaaS (capture → extract → classify → route)
- Resonant Knowledge Graph (resonate / inhibit / excite; temporal GraphRAG)
- MCP surface + ECF board wiring
- LAM service (v1 channels: risk, urgency, customer impact, compliance)
- Policy/Audit (RBAC, redaction, snapshots)

**Out‑of‑scope (v1)**
- Robotics/hardware, luxury installs, generalized consulting
- Unbounded custom dashboards (unless they feed the platform)

Guardrails: data residency honored; PII redaction enforced in pipeline.

---

## 2) Simplify to SKUs (Susanna — Simplify)
- **S1: Smart‑Filing Core (SaaS)** — connectors (Drive/SharePoint/Box/Slack/Email), IDP extraction, classification, routing, logging.
- **S2: Coherency Graph Add‑On** — resonant edges + scored traversal + feedback updates.
- **S3: Compliance Pack (opt.)** — redaction, policy checks, audit export.

**Acceptance criteria (per pilot)**
- Filing accuracy ≥ **95%** on pilot corpus
- Time‑to‑find document **–50%**
- Zero PII leaks in redaction tests

---

## 3) Two‑Week Sprint (Ivy — Accelerate)
> Ship something tangible **daily** (artifact/API/demo clip).

| Day | Deliverable |
|---|---|
| 1 | Ingestion skeleton + connector stubs |
| 2 | OCR/IDP wiring (baseline) |
| 3 | Field mappers per workflow |
| 4 | Classifier v1 + routing rules |
| 5 | Event logging schema (BrainSTEM) |
| 6 | Graph store up; edge schema |
| 7 | Scored traversal + feedback delta |
| 8 | MCP endpoints live |
| 9 | ECF wiring; pulse logs |
| 10 | LAM svc v0 (risk/urgency/customer/compliance) |
| 11 | Demo corpus + metrics harness |
| 12 | Security pass (RBAC, redaction, audit) |
| 13 | Pilot env + sample paths |
| 14 | Dry‑run demo + fix list |

---

## 4) Automations & Interfaces (Aspen — Automate)
**Services (MVP)**
- `tongue.ingest` → store + index + emit event
- `idp.extract` → key fields
- `classify.route` → folder/tags/owner + webhook
- `graph.upsert_edge_attr` → polarity + weight (+time)
- `graph.traverse_scored` → top‑k path
- `feedback.update_edges` → apply delta
- `policy.check` / `audit.snapshot`
- `lam.read_channels` / `lam.subscribe`

**Instrumentation**
- Every action emits: `{doc_id, step, persona, lam_state, graph_deltas, latency}`

**Packaging**
- Docker images per svc; Helm/Compose for pilots
- MCP manifest for discoverability
- ECF board controls exposed: `board.activate`, `board.pulse`, `board.status`

---

## 5) Demonstrate (Sophie — Demonstrate)
**Demo storyline (8–10 min)**
1. Pre‑us pain (missed clauses, slow retrieval)
2. Live capture → extract → file
3. Graph view with **resonate/inhibit/excite**
4. Live correction → feedback updates edge weights → re‑query improves
5. Compliance snapshot (redaction + policy pass + audit log)
6. Metrics (accuracy, speed, zero‑leak)
7. One‑click export to client systems

**Assets**
- Landing page (one‑liner, 3 bullets, 90‑sec video)
- 3 screenshots (capture, graph, compliance)
- ROI calc + pilot SOW + security brief
- Outreach kit (5‑email sequence + LinkedIn blurb)

---

## 6) Endure (Morgan — Endure)
**Cadence**
- Daily pulse (7 min): what shipped, what’s stuck
- Weekly ship list: visible in repo
- Sundays on until revenue covers fixed costs

**KPIs**
- 2 weeks: MVP demo complete
- 60 days: 2 pilots live; ≥95% accuracy; –50% time‑to‑find
- 90 days: ≥ $200k ARR from conversions; case study published

**Risk register**
- Track: privacy, IT approvals, model regressions, scope creep
- Mitigations: DPA, RBAC/tenancy, redaction tests per release, out‑of‑scope policy

---

## 7) Checklists

### Daily
- [ ] One tangible ship (artifact/API/demo)
- [ ] Pulse log written (events + metrics)
- [ ] Security checks passed for changed services

### Weekly
- [ ] Publish ship list + demo clip
- [ ] Review KPIs vs targets
- [ ] Triage risks; update mitigations

### Release Gate (pilot)
- [ ] Accuracy ≥95%
- [ ] TTF –50%
- [ ] Redaction/Policy/Audit verified
- [ ] Demo storyline rehearsed

---

## 8) Repo Pointers
Suggested tree:
```
/docs/operator/Operator_Plan_IndustryCoherence_v1.md
/docs/demos/demo_script.md
/runbooks/checklists.md
/runbooks/risk_register.csv
/sprints/sprint_board_14day.csv
```
