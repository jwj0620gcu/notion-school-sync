-- Run after 001_init.sql
-- Adds analysis table used by report.py in Supabase mode

create table if not exists public.analysis (
  id bigserial primary key,
  user_id uuid not null references public.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  snippet_count integer,
  burnout_risk integer,
  team_health integer,
  diligence integer,
  recurrence integer,
  growth integer,
  execution integer,
  emotional_energy integer,
  details_json jsonb not null default '{}'::jsonb,
  alert_days jsonb not null default '[]'::jsonb,
  improvement_areas jsonb not null default '[]'::jsonb,
  positive_trends jsonb not null default '[]'::jsonb,
  overall_summary text,
  notion_page_id text
);

create index if not exists idx_analysis_user_created_at
  on public.analysis(user_id, created_at desc);
