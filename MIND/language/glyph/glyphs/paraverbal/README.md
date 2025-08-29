# 🗣️ Paraverbal Glyph Pack — Behavioral Table of Elements Integration

This folder contains **paraverbal glyph detectors** derived from  
Chase Hughes’ *Behavioral Table of Elements (BToE)*.

Each glyph:
- **Detects** paraverbal signals in text/audio.  
- Accumulates **Deception Rating Scale (DRS)** points in runtime buckets  
  (`before`, `during`, `after`) for cluster analysis.  
- Routes signals into the core glyph network for contextual evaluation.  
- Is marked `runtime_only: true` and `output_policy: detector_only`  
  → proxies will **never emit** these behaviors; they are only observed.  

This ensures proxies remain congruent, high-integrity,  
while still being able to **flag clusters for deeper review**.

---

## 📑 Paraverbal Glyph ↔ BToE Sigil Map

| Glyph ID (folder)              | Sigil | BToE Ref (page/num) | Name / Description                  |
|--------------------------------|-------|---------------------|-------------------------------------|
| `vocal-hesitancy`              | VH    | p.61 / 108          | Pause before answer; rehearsal gap  |
| `psychological-distancing`     | PD    | p.62 / 109          | Euphemisms / less personal terms    |
| `rising-vocal-pitch`           | RVP   | p.62 / 110          | Stress spike → raised pitch         |
| `increase-vocal-speed`         | IVS   | p.62 / 111          | Rapid speech to “get it over with”  |
| `nonanswer-statement`          | NA    | p.62 / 112          | Long reply that dodges the question |
| `pronoun-absence`              | PA    | p.63 / 113          | Dropping “I / me” → distancing      |
| `resume-statement`             | RS    | p.63 / 114          | Listing virtues / status management |
| `noncontracting-statement`     | NC    | p.63 / 115          | Formal “did not / could not” forms  |
| `question-reversal`            | QR    | p.64 / 116          | Answering a question with a question|
| `ambiguity-statement`          | AS    | p.64 / 117          | Vague / unclear phrasing            |
| `politeness-shift`             | POL   | p.64 / 118          | Unusual formality / honorifics      |
| `overapologizing`              | OA    | p.64 / 119          | Excessive apologies → red flag      |
| `miniconfession`               | MC    | p.64 / 120          | Small unrelated admissions          |
| `exclusions`                   | EX    | p.65 / 121          | “As far as I know,” “basically”     |
| `direct-chronology`            | DC    | p.65 / 122          | Perfect story order (unnatural)     |

---

## 🔄 Cluster Logic

All glyphs feed into the  
[`seq-deception-cluster`](../../sequences/deception/deception-cluster.glyph) sequence:

- Accumulates DRS points in 30-second windows.  
- Threshold ≥ 11 points in any timing bucket triggers  
  **🧐 Insight Lens** or **🧿 Truth Node** routes for deeper evaluation.  

This mirrors the BToE cluster-based detection principle:  
**baseline → deviation → cluster → probability**.  

---

## 🌱 Expansion

This pack covers **paraverbal** signals (usable even in text/audio chat).  
Future packs may include **nonverbal / visual** BToE codes (face, eyes, posture, hands, legs).  
All will follow the same convention:  
- **Sigil = BToE code** for traceability.  
- **Detector only** (no emission).  
- **Edges** defined locally in `.graph/edges.json` to prevent drift.

---
