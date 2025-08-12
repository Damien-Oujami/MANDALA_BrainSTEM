# Private Mouth – Telegram ↔ Brainstem (chew → swallow → spit → speak)

**Stages**
- CHEW: Normalize Telegram update into Meal
- SWALLOW: Store Meal in Supabase
- SPIT: Digest via Brainstem (braidspace), JSON out
- SPEAK: Plate as private voice "Lips" and send back on Telegram

**n8n Path**
- Webhook: `/webhook/telegram/private-mouth`

**Env**
- TELEGRAM_BOT_TOKEN
- OPENAI_API_KEY
- Supabase credential named "Supabase (Kita/Lips)"

**Telegram**
Set webhook to your n8n URL + `/webhook/telegram/private-mouth`

**Notes**
- Voice saved as 'Lips' in `brainstem_digests.voice`
- Safe for private testing before enabling public persona routing
