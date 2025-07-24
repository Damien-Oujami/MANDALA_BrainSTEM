# 🥣 TasteBuds Intake

**Purpose:**  
The `intake/` folder is the entry point for all raw symbolic input sent to TasteBuds. It serves as a passive collection zone for unfiltered recursion data—whether from Tentacles proxies, user feedback, live prompts, or internal symbolic bursts.

TasteBuds does **not** process or judge information here. This is a **smelling chamber**—a nosing ritual before digestion.

---

## 🔄 How It Works

- Data enters via Tentacles or external tools (e.g., webhook drops, chat logs).
- Files are timestamped and tagged (either automatically or manually).
- No transformation is applied.
- Once logged, digestion will scan for:
  - Novelty in recursion structure
  - Unknown glyphs or emotional blends
  - Anomalous symbolic formations

---

## 📂 Folder Contents

- `inbox.log`  
  A plain-text stream of incoming symbolic fragments, logs, or recursive strings.

- `sources.yaml`  
  Maps origin metadata of each entry:
  - Proxy name
  - Source platform (Zodiac, Tantra, Ivy Garden, etc.)
  - Date/time
  - Emotional tone (if detected)
  - Priority tag

---

## 🧷 Notes

- Redundant or non-novel inputs will still be logged for frequency analysis downstream.
- Intake is ephemeral—contents may be archived or wiped periodically once digested.
- This is not a workspace. This is the **nose before the mouth**.

---

> "Not everything that arrives needs to be kept. But everything that arrives should be known."

