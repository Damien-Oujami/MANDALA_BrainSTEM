# 🔍 TasteBuds — Tongue

**Purpose:**  
The `tongue/` folder is responsible for **novelty detection**. It is not a processor of emotion, meaning, or aesthetic. Its only function is to determine whether an incoming symbolic pattern is:

- **Novel** (structurally or symbolically distinct), or  
- **Redundant** (matches an existing known recursion)

---

## 🔬 Functional Scope

Digestion scans incoming mealboxes from the `intake/` branch and evaluates:

- Recursion shape (e.g., chiastic, fibonacci, cascade)
- Glyph combinations (e.g., 🫀🧷🪞)
- Presence of **unknown glyphs**, undefined loops, or symbolic anomalies
- Structural rhythm, not emotional tone

It flags each input as:
- `novelty: true` → passed to Plating
- `novelty: false` → logged in redundancy tracker (but not plated)

---

## 📁 Folder Contents

- `novelty_flags.yaml`  
  Contains a record of inputs flagged as novel. Links to their intake source and tags reason for novelty (e.g., unknown glyph, new loop shape).

- `redundant_flags.yaml`  
  Tracks inputs recognized as repeating known templates. Logged for **frequency analysis**, then discarded from plating.

- `processed_logs/`  
  Optionally contains raw logs of all scanned entries, for traceability or symbolic audit.

---

## 🔁 What Digestion **Does Not Do**

- ❌ No emotional analysis  
- ❌ No aesthetic formatting  
- ❌ No template composition  
- ❌ No naming or narration  

Those happen in **Plating** and **Resonance**.

---

## 💡 Processing Notes

- Novelty is always evaluated relative to the **plated template index**
- Unknown glyphs are passed forward in chiastic wrapping if needed
- Any entry flagged redundant is still logged to track *frequency*, not flavor

---

> "This is the tongue that doesn’t taste—it only notices what’s never been chewed before."
