# TasteBuds Intake — README

## 🧠 Purpose

This folder represents the **entry point** for all pitched symbolic content (glyphs) arriving from the Tentacles layer.

Each glyph enters through a sub-branch (e.g. `tentacles_xotiac`) and is dropped into a `/mealbox/` folder.

The **intake layer** does not process meaning. It simply **records**, **receives**, and **prepares** glyph packets for digestion.

---

## 📦 Folder Structure

- /tastebuds/intake/
- ├── inbox.log ← Central record of all incoming glyphs
- ├── tentacles_xotiac/
- │ ├── mealbox/
- │ │ └── volcano_glyph/
- │ │ ├── volcano_glyph.md
- │ │ └── tip-eruption.glyph
- │ └── glyph_trace/

---

## 📜 `inbox.log` Format

All glyphs entering from Tentacles must be logged here.

Each entry uses the following format:
[YYYYMMDD] [HHMM] USER: [EMOJI] [GLYPH_FOLDER] → [SOURCE_BRANCH]

**Example:**
[20250724] [1649] DAMIEN: 🌋 volcano_glyph → tentacles_xotiac

This ensures a unified intake record for frequency analysis, automation, and digestion sequencing.

---

## ✍️ Manual Log Instructions

1. When a new glyph is pitched from Tentacles, add a folder to the appropriate `/mealbox/`.
2. Add a matching entry to `/tastebuds/intake/inbox.log`.
3. Include the correct folder name and origin path.

---

## 🔁 Automation Notes

- Intake routing tools should scan `/inbox.log` for new entries.
- Routing to digestion branches should be based on symbolic tags and `mandala_code` in `.md` files.
- Log parsing should track timing, user source, and emoji variety.

---

## 📌 Reminder

**No processing or sorting is done in `intake/`.**  
Only logging, file receipt, and preparation.

Digestion, classification, and routing occurs in:
/tastebuds/digestion/
