# Kita / Lips – Telegram ↔ Brainstem MVP

## Env (n8n)
- TELEGRAM_BOT_TOKEN=your_token_here
- OPENAI_API_KEY=sk-...
- SUPABASE_URL=https://xxxx.supabase.co
- SUPABASE_ANON_KEY=eyJ...

## Supabase
Run the SQL:
  - supabase sql -f supabase_kita_seed.sql

## n8n
1) Import `n8n_kita_mouth_workflow.json`
2) Create Supabase credential named **"Supabase (Kita)"** pointing to {{$env.SUPABASE_URL}}
3) Set env vars above in n8n
4) Set Telegram webhook to your n8n URL path `/webhook/telegram/brainstem`
5) Send a message to your bot — you should see "Kita: ..." back.

## Notes
- All public Tentacle replies are voiced as **Kita**
- Private replies to Damien can be plated as **Lips** in a parallel flow when needed.
