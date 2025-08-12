-- Supabase seed for Kita/Lips Telegram loop
create table if not exists mealbox_intake (
  meal_id text primary key,
  source text not null,
  chat_id bigint not null,
  user_id bigint not null,
  username text,
  ts timestamptz not null,
  payload jsonb not null,
  context jsonb,
  flags jsonb,
  created_at timestamptz default now()
);

create table if not exists brainstem_digests (
  meal_id text primary key references mealbox_intake(meal_id) on delete cascade,
  anidex jsonb not null,
  tendrils jsonb not null,
  reply jsonb not null,
  log jsonb,
  voice text default 'Kita',
  created_at timestamptz default now()
);

create table if not exists thread_memory (
  thread_key text primary key,
  recent_messages jsonb default '[]'::jsonb,
  last_seen timestamptz default now()
);
