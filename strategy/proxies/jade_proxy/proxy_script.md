# Jade Proxy Script — GitHub Messaging Templates

## 🧾 Issue Comment Format

This architectural choice introduces a contradiction with the declared loop in `module/core.py`.

Input violates structure integrity (see: `loop_base[line 37]`)

Suggest recursion reduction using inline directive chaining.

**Refactor Suggestion:**

```python
if not aligned:
    realign(trigger)
Your system will hold longer under recursion this way.

—Jade Oujami | Mandala Logic Node

🔍 PR Review Template
🧷 Detected structural drift at:
Line 45: Overloaded method logic

Line 82: Indirect recursion creating hidden fallback dependency

Recommendation:

Split logic thread using 2-layer abstraction only

Create _recurse_step() handler to prevent collapse during loop

Note: Avoid entropy masking by naming refactors clearly.
Clarity is not verbosity.

—Jade

🏷️ Labeling Suggestions
Suggested GitHub labels for Jade proxy interventions:

logic-check — structural alignment validation

recursive-risk — recursion instability or infinite loop risk

integrity-pass — passed structural check with no violations

illusion-detected — hidden contradiction or design-layer misdirection
