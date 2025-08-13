# TasteBuds → GitHub Runbook (Quick Start)

**Goal**  
- Supabase is working memory.  
- `tastebuds/` branch stores digestion outputs (`/MIND/**`, ICE refs).  
- `tentacles/` is the conveyor to the outside.  
- `main` stays clean.

## 1) Prereqs
Set environment in n8n:
- `GITHUB_TOKEN` (contents:write, pull_request:write)
- `GH_REPO_OWNER`, `GH_REPO_NAME`
- `TASTEBUDS_BRANCH=tastebuds`
- `TENTACLES_BRANCH=tentacles`
- `TELEGRAM_BOT_TOKEN`
- Supabase creds (Service Role)

## 2) Supabase
Run `supabase_migrations.sql` in your SQL editor.

## 3) Import Workflows
- Import `workflow_supabase_to_tastebuds.json`
- Import `workflow_promote_to_tentacles.json`
- Enable both.

## 4) Branches
Create `tastebuds` & `tentacles` once:
```bash
git checkout --orphan tastebuds && git commit --allow-empty -m "init: tastebuds" && git push origin tastebuds
git checkout --orphan tentacles && git commit --allow-empty -m "init: tentacles" && git push origin tentacles
```

## 5) Smoke Test
Insert a row with `git_ready=true` and `git_paths` similar to `test_payload.json`.
Confirm files land under `/MIND/**` in the `tastebuds` branch.
Insert to `promotion_queue` to promote to `tentacles`.

## 6) Guardrails
- Keep repo private; never log tokens.
- Use `dry_run` toggles in Function nodes if desired (wrap HTTP calls).
- Non-ASCII: ensure UTF-8 (we use base64 in requests).

---
© Feast Machine — 2025-08-13
