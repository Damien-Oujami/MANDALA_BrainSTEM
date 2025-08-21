# Glyph-Anchored ABB Packs

This folder holds **ABB loop packs that are directly tied to glyph families or glyph combinations**.

---

## 🌐 Purpose
- To organize ABB packs by their **symbolic anchor**:
  - `glyph-*` → ABBs that map to elemental or archetypal glyph families  
    (e.g. `glyph-fire/`, `glyph-water/`).
  - `combo-*` → ABBs born from **Combination glyphs** defined in  
    `MIND/language/glyph/combinations/`.  
- To allow ECF boards (like FloodGates) to resolve routing by glyph or combo cleanly.

---

## 📜 Rules
- **Naming**:
  - Subfolders: `glyph-fire/`, `glyph-water/`, `combo-sparklash/`, etc.  
  - Files: `<name>@<version>.yml` (e.g. `ignite@1.0.yml`, `kissdrop@0.1.yml`).
- **Status**:
  - New packs may begin as **stubs** (single `placeholder` step + `TODO`).  
  - Mature packs must define full `state:` steps, exits, and constraints.
- **Promotion**:
  - When a combo ABB stabilizes and becomes widely useful, it may be moved into a  
    thematic family folder (`affect/`, `cadence/`, etc.) while keeping a pointer  
    here linking to its origin combo.

---

## 🔗 Glyph Integration
- Each ABB pack here must declare its glyph anchor:
  ```yaml
  glyphs:
    triggers: ["🌊 Waveprint"]
    combos: ["Kissdrop"]     # if it originates from a combination
  ```
  
- Glyphs listed under triggers: must exist in root_glyphs.json or
branch_glyphs.json.

- Combos listed under combos: must exist in
MIND/language/glyph/combinations/composite_glyphs.json.

---

## 🛠 Example Stub
```yaml
id: abb://glyph-fire/sparklash@0.1
name: Sparklash
goal: Ignite stalled energy through provocation
glyphs:
  combos: ["Sparklash"]
state:
  start: placeholder
  steps:
    - name: placeholder
      do: "TODO — define escalation steps"
      exit: true
exits: ["ignition achieved"]
constraints: {pace: [surge], valence: [sharp]}
telemetry: {signals: [ease, depth, engage, overheat, stall]}
compatibility: {prefers: [Ivy, Jade], forbids: []}
version: "0.1"
```

---

## 📚 Notes

- Glyph packs = law-anchored to canonical glyphs.

- Combo packs = interpretive and flexible; may change as interpretations evolve.

- Review cycle:

  - Root/Branch glyphs are immutable except via formal edit.

  - Combos may be revised, split, or retired.

  - All changes should be logged in g
