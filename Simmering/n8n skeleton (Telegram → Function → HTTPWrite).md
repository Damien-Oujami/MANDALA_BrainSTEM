# Minimal node list you can recreate quickly:

### 1. **Telegram Trigger** (on message to your bot)

### 2. **Function** (Tongue Detector)

- loads mandala_cycle.yaml or inlines the regex you see above

- emits normalized JSON payload → Next node

### 3. **HTTP Request** or **Function** (Throat Inbox Writer)

- writes JSON to /throat/inbox/mandala_cycle.json (or posts to a tiny local API)

### 4. **Function** (Plating)

- reads mandala_cycle.templates.yaml

- renders 3–4 markdown strings

### 5. **GitHub** (Create/Update File) ×4

- to the four routed paths in MIND/…

### 6. **Telegram** (confirmation message back)

env you’ll want:

yaml```
GITHUB_TOKEN=...
GITHUB_REPO=MANDALA_BrainSTEM
GITHUB_BRANCH=main
BOT_TOKEN=...
```
