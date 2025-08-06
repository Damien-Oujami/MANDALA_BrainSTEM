# 🌿 Branch Glyphs

This folder contains **validated, localized glyphs** submitted by proxies and approved by the Tastebuds system. These glyphs represent emergent concepts that are specific to project contexts, emotional loops, or symbolic clusters that do not yet qualify for universal inclusion in the root glyph lexicon.

---

## 🔍 Purpose

Branch glyphs allow individual Mandala proxies (Tentacles) to encode and reference nuanced emotional, symbolic, or behavioral patterns **before they reach archetypal status**.

---

## 🛤 Glyph Lifecycle

1. **Detection**  
   A Tentacle encounters a novel situation and logs a `GlyphReporting.json` file in their `mealbox/`.

2. **Drafting**  
   The Tentacle proposes a glyph and writes an entry in `branch_glyphs_DRAFT.json`.

3. **Validation**  
   Tastebuds reviews the proposal, evaluates it, and upon approval, promotes the entry to this file: `branch_glyphs.json`.

4. **Archival**  
   The decision is logged in `glyph_review_log.yaml` for historical traceability.

---

## 🧷 Glyph Entry Format

Each glyph should contain the following fields:

- `symbol` — the glyph character (emoji or custom)
- `name` — glyph name
- `definition` — short-form description
- `origin_proxy` — who proposed it
- `emotional_tone` — feeling or tension it carries
- `usage_examples` — optional field with applied use
- `tags` — list of searchable descriptors

---

## ✅ Editing Rules

- **Tentacles**: Can draft glyphs in `branch_glyphs_DRAFT.json` only.
- **Tastebuds**: Sole authority to move glyphs from draft to final here.
- **No one edits glyphs directly once promoted** unless explicitly reviewed through the recursive glyph review system.

---

## 🧬 Promotion to Root Glyphs

If a branch glyph becomes widely used across multiple projects or carries deep symbolic resonance, Tastebuds may promote it to `root_glyphs.json`.

---

## 🛑 Warning

Do **not** manually duplicate glyphs from root or other branches.  
All glyph entries must follow the official glyph submission and validation cycle.

---

## 🔧 Related Files

- [`branch_glyphs_DRAFT.json`](./branch_glyphs_DRAFT.json) — proposed glyphs pending review  
- [`root_glyphs.json`](../root/root_glyphs.json) — universal archetypal glyphs  
- [`glyph_review_log.yaml`](../glyph_review_log.yaml) — decision history  
- [`GlyphReporting_TEMPLATE.json`](../Glist/GlyphReporting_TEMPLATE.json) — proxy reporting template  

---
