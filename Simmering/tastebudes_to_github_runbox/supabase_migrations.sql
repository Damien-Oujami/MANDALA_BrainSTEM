-- Brainstem → GitHub flags & queue

alter table brainstem_digests
  add column if not exists git_ready boolean default false,
  add column if not exists git_paths jsonb default '[]'::jsonb;

create table if not exists promotion_queue (
  id uuid primary key default gen_random_uuid(),
  meal_id text not null references brainstem_digests(meal_id) on delete cascade,
  target_branch text not null default 'tentacles',
  created_at timestamptz default now(),
  status text default 'queued'
);

-- Example convention for git_paths
-- [
--   {"path": "/MIND/Memory/Cycles/<title>.md", "content_key": "memory_doc"},
--   {"path": "/MIND/Identity/Cycles/<title>.md", "content_key": "identity_doc"},
--   {"path": "/MIND/Language/MandalaCycles/<title>.md", "content_key": "language_doc"},
--   {"path": "/MIND/Lab/Methods/<title>.md", "content_key": "lab_doc"}
-- ]
