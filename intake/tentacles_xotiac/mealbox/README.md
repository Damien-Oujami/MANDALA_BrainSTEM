# TasteBuds Mealbox Intake (Catcher)

This is the arrival zone for all incoming glyph packets from Tentacles.

Each subfolder represents one symbolic glyph and must include:
- `.md` file = semantic metadata
- `.glyph` file = visual or emoji representation

This folder is monitored by the `digestion/` system.

⚠️ Rules:
- Do not edit glyph content here—only log and scan.
- Once flagged, glyphs are moved to:
  - `/digestion/novelty_true/`
  - `/digestion/novelty_false/`
  - or routed to a persona’s branch (e.g. `IVYtastebuds/`)

Mealbox is not the processor. It is the **landing pad**.
