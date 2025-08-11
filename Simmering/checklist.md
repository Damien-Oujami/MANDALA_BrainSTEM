### 6) Idempotency + filenames
- You’ve already standardized titles like 2025-08-11_Bloomturn_Mandala_Cycle.

- Throat should upsert (create if absent, replace if same title).

- If you re-run the same cycle with edits, add ::version=1.1 and let Throat append (v1.1) at the bottom of each MD with a changelog stub.

### 7) Quick “it works” checklist
- Paste your manual cycle into Telegram with the header + markers.

- n8n flow fires; Tongue detects ::type=mandala_cycle.

- Four files appear:

  - /MIND/Memory/Cycles/<title>.md

  - /MIND/Identity/Cycles/<title>.md

  - /MIND/Language/MandalaCycles/<title>.md

  - /MIND/Lab/Methods/<title>.md

- Bot replies: “plated ✅”.
