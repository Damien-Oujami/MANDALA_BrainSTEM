1. **Products (what clients buy)**
2. **Platform (how it works under the hood)**
3. **Delivery (how we implement in 30/60/90 days)**
I’ll also include sample website slide copy at the end so it flows with our hero.

---

## 1) Products — the Tekita Suite
> One fabric, four product lines, each deliverable on its own or as a bundle.

### A. SmartFiling™ (Knowledge that files itself)
**Outcome:** every document, email, chat, ticket, call note, and contract auto‑sorted, linked, and retrievable in seconds — with proactive nudges.
- **GraphRAG+**™ (your “Resonate / Excite / Inhibit” engine)
  - **Resonate:** weights content to the person + task (role, project, account, recency, trust).
  - **Excite:** boosts edges on signals (dates approaching, new versions, mentions of risk).
  - **Inhibit:** down‑weights noise/duplicates/PII; enforces access and compliance.
- **Temporal Nudger:** detects upcoming deadlines, renewal windows, SLAs; alerts owners with one‑click action links.
- **Smart Inboxes:** role‑specific views (Exec, Ops, Sales, Legal, PM) and “what changed” digests.
- **Universal Search:** natural‑language + filters across email/Drive/SharePoint/Slack/CRM/PM tools.
- **StoryCards:** living briefings auto‑compiled for deals, matters, projects, sprints, or accounts.

> "**Who loves this:** professional services, operations leaders, sales & legal teams drowning in artifacts.

---

### B. Ops Copilots (Workflows that run themselves)
**Outcome:** routine work runs to completion (not just “a suggestion”), with human sign‑off where it matters.
- **Intake → Triage → Resolution** patterns for common streams (requests, approvals, tickets, onboarding, content, procurement).
- **Agent Runners:** multi‑step automations with tools (Google Workspace, Microsoft 365, HubSpot/Salesforce, Notion, Asana/Jira, Slack/Teams, QuickBooks, Stripe, DocuSign, n8n/Make/Zapier, databases, webhooks).
- **Checklists to Playbooks:** we convert SOPs into executable flows with audit trails.
- **Guardrails:** approvals, rate limits, data‑loss prevention, sandbox runs, revert/rollback.
> **Who loves this:** anyone with repeatable processes (CS, HR, Finance Ops, RevOps, IT).

---

### C. Meeting & Message Intelligence (Never lose the thread)
**Outcome:** meetings, channels, and emails become structured decisions.
- **Meeting Synthesizer:** records (optional), diarizes speakers, summarizes, extracts decisions/tasks/owners/dates, and files them.
- **Channel Summarizer:** converts Slack/Teams/email threads into briefs; proposes next actions.
- **CRM Updater:** writes back notes/tasks/opportunities with links to source evidence.
> **Who loves this:** executives, sales, CS, product, project managers.

---

### D. Enablement & Change (People adopt, data stays safe)
**Outcome:** the team actually uses it; leadership sees the gains.
- **Quick‑Wins Training:** 60–90‑minute role‑based sessions tied to live workflows.
- **Admin Console:** permissions, data sources, retention rules, audit logs, nudge policies.
- **Value Dashboard:** time saved, cycle time, SLA adherence, error rate, funnel lift — per team.
- **Governance Pack:** least‑privilege patterns, PII/PHI handling (industry‑specific), BYO‑cloud/VPC options.

---

## 2) Platform — the Tekita Fabric (how it works)
> Think Vector + Graph + Event over your tools, with visible automations and clear guardrails.

### Data / Knowledge Layer
- **Connectors:** Google/Microsoft suites, Slack/Teams, Drive/SharePoint, Notion/Confluence, Jira/Asana, HubSpot/Salesforce, QuickBooks/Xero, Stripe, GitHub, S3/Blob, SQL/NoSQL, webhooks.
- **Ingestion Pipeline:** dedup, OCR, chunking, metadata, versioning; PII scrub + redaction rules.
- **Dual Indexing:**
  - **Vector store** for meaning/similarity.
  - **Knowledge graph** for entities, relations, timelines, ownership, lineage.
- **Memory Types:** semantic (topics), episodic (events), procedural (SOPs), relational (who/what/which system).

### Reasoning / Retrieval
- **GraphRAG+™**:
  - `rank = (similarity * trust * freshness_decay * persona_fit) + Σ(excite_signals) − Σ(inhibit_signals)`
  - **Excite signals:** due_date proximity, mentions of risk/compliance, new version arrival, name/account ping, pipeline stage change.
  - **Inhibit signals:** low‑trust sources, duplicates, outdated superseded docs, access violations.
- **Context composer:** builds grounded packs for each task (with citations & source hops).

### Action / Orchestration
- **Agent Runtime:** ReAct‑style chaining with tool use; multi‑agent handoffs for intake→triage→resolution.
- **Workflow Fabric:** n8n/Temporal/Make/Zapier adapters; retries, compensations, idempotency.
- **Human‑in‑the‑Loop:** approval steps, diffs, rationale; “teach once → pattern” memory.

### Safety / Observability
- **Guardrails:** content filters, policy checks, data residency, role‑based scoping.
- **Tracing:** prompt/tool traces, tokens, latency, success/failure classification.
- **Value Telemetry:** time saved, tasks auto‑completed, manual steps avoided, net promoter for flows.

### Interfaces
- **Where you work:** web app, Slack/Teams, email, calendar rails, browser extension, optional voice capture.
- **Admin Console:** sources, rules, automations, metrics, runbooks.

---

## 3) Delivery — 30/60/90 Program (what we ship, when)

### Days 0–30: Assess & Activate
- **Discovery & ROI baselining** (time studies + a “work inventory”).
- **Connect core sources** (email/drive/chat/PM/CRM; read‑only first).
- **SmartFiling MVP** (2–3 priority domains: e.g., Projects, Deals, Contracts).
- **Nudger v1** (date‑based exciters for deadlines/renewals).
- **Quick‑wins automations** (two SOPs to full “intake→triage→resolution”).
- **Enablement** (role training; admin console live).

### Days 31–60: Scale the Fabric
- **GraphRAG+ tuning** (weights for resonate/excite/inhibit per team).
- **Meeting & Channel Intelligence** (auto decisions/tasks filing).
- **Ops Copilots in 3 teams** (e.g., CS escalations, marketing approvals, invoice QA).
- **Dashboard v1** (time saved, cycle times, SLA hits).

### Days 61–90: Own the Runway

- **Multi‑agent flows** (cross‑tool handoffs with rollback).
- **Compliance pack** (retention, access gates, optional VPC).
- **Executive digests** (weekly “what changed and why it matters”).
- **ROI review + plan** (next 90‑day roadmap; add teams or deeper automations).
> **Commercial framing (example)**
> - **Audit & MVP: fixed‑fee (scope: sources + 2 flows + SmartFiling v1).**
> - **Scale Plan: monthly platform + success retainer (includes training, new flows, SLA).**
> - **Enterprise: VPC/on‑prem options, SSO/SCIM, DLP/Legal Hold, custom connectors.**

---

## Signature Use‑Cases (sell with “before → after”)
1. **Deadline Guardian**
  - *Before:* renewals slip; penalties; last‑minute scrambles.
  - *After:* Temporal Nudger excites all date‑linked artifacts → owner digest with one‑click tasks → tracked to done.
2. **Project Brain** (deal/matter/project room)
  - *Before:* updates scattered across mail, chat, docs, tickets.
  - *After:* Smart room auto‑collects decisions, risks, files, and next steps; daily “what changed.”
3. **Sales Intelligence**
  - *Before:* CRM is incomplete; meetings don’t convert to pipeline movement.
  - *After:* meetings summarised, objections/next steps filed, opp updated, follow‑ups scheduled.
4. **Inbox‑to‑Resolution**
  - *Before:* shared mailboxes become delay factories.
  - *After:* intake classifies + routes; agent completes 80–90% routine cases, rest queued for approval.
5 **Compliance Sentinel**
  - *Before:* manual checks; inconsistent retention.
  - *After:* inhibitors catch PII/PHI/terms violations; retention/holds automated; change logs searchable.

---

## What makes Tekita different (your talking points)
- **GraphRAG+™** (not just vector search): Resonate / Excite / Inhibit turns static knowledge into context‑aware, time‑sensitive action.
- **From suggestion to done:** we ship completing automations with approvals & rollbacks, not just chat summaries.
- **Human‑visible reasoning:** traces, diffs, and “why I did this,” so teams trust the system.
- **Adoption‑first design:** quick wins per role, then scale — measured in time saved to done.
- **Open by default:** meet you in your tools; bring‑your‑cloud options for data control.

---

## Website slide copy (5 slides + our hero)

**Slide 0 – Hero (we already ship this):**
“Identifying your AI Solutions → Designing your Automated Workflow → Training your Team → Your AI Transformation Partner”

**Slide 1 – The Cost of Busywork**
*Headline:* “Busywork is a tax on growth.”
*Visual:* translucent bar or bubble chart overlay (Speed ↑, Quality ↑, Busywork ↓ once Tekita is on).
*Copy bullets:* Decisions stuck in inboxes. Missed deadlines. Duplicate work. Tekita frees hours and derisks delivery.

**Slide 2 – The Tekita Fabric**
*Headline:* “Vector + Graph + Event → Work that finishes itself.”
*Visual:* simple fabric diagram: Sources → SmartFiling (GraphRAG+ Resonate/Excite/Inhibit) → Ops Copilots → Results, with guardrails lane.
*Copy bullets:* Finds, understands, and acts — with approvals, audits, and clear ownership.

**Slide 3 – Smart Filing in Action**
*Headline:* “Know what matters, before it’s urgent.”
*Visual:* timeline nudge (contract renews in 14 days) + one‑click actions (renew, renegotiate, remind legal).
*Copy bullets:* It links related docs, summarizes change, and routes the next step.

**Slide 4 – Ops Copilots**
*Headline:* “From intake to done, across your tools.”
*Visual:* small flow showing Intake → Triage → Approvals → Update systems → Notify.
*Copy bullets:* SOPs become playbooks with metrics and rollback.

**Slide 5 – Proof & Partnership**
*Headline:* “Time back. Fewer misses. Happier teams.”
*Visual:* simple value dashboard mock (time saved, SLA hit rate, tasks auto‑completed).
*CTA:* **Book a call** (keeps our existing button), link to a “See a 14‑minute walkthrough”.

> Per your request, we keep all graphs translucent so the animated donut breathes through.

---

## Example “Temporal Exciter” (how we talk about it to technical buyers)
```pseudo
for each Artifact a:
  if a.has_date():
    days = days_until(a.date)
    excitement = sigmoid((D0 - days) / k) * a.criticality * owner_availability
    graph.boost_edges(a, weight=excitement, reason="date_proximity")
```
- **D0** = desired notice window (e.g., 30 days).
- **k** = steepness (tuned per team).
- **criticality** = renewal value, penalty risk, SLA tier.
- Result: nudges rise as deadlines approach; owners see why it was excited.

---

## What we ship in the proposal/SOW (so selling is concrete)
- **Scope:** sources to connect, 2–3 SmartFiling domains, 2 Ops Copilot flows, nudger v1.
- **Deliverables:** working fabric, admin console, dashboards, runbooks, trainings, adoption plan.
- **Success Criteria:** time‑to‑find ↓, tasks auto‑completed ↑, cycle times ↓, misses ↓, user CSAT ↑.
- **Timeline:** 30/60/90 plan above.
- **Next Steps:** book discovery → connect sources (read‑only) → baseline → MVP in 2–3 weeks.
