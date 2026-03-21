-- Run this in Supabase SQL Editor

create extension if not exists pgcrypto;

create table if not exists public.users (
  id uuid primary key,
  email text unique,
  display_name text,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.user_settings (
  user_id uuid primary key references public.users(id) on delete cascade,
  notion_token_enc text,
  notion_page_id text,
  school_api_key_enc text,
  gemini_api_key_enc text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.snippets (
  id bigserial primary key,
  user_id uuid not null references public.users(id) on delete cascade,
  snippet_date date not null,
  source text not null default '1000school',
  content text,
  health_score numeric(4,1),
  feedback_score integer,
  highlights text,
  lowlights text,
  tomorrow_goals text,
  team_mentions text,
  learnings text,
  external_id text,
  synced_at timestamptz not null default now(),
  unique (user_id, snippet_date)
);

create table if not exists public.user_state (
  user_id uuid primary key references public.users(id) on delete cascade,
  last_notion_check_at timestamptz,
  last_notion_sync_at timestamptz,
  last_weekly_report_at timestamptz,
  last_monthly_report_at timestamptz,
  last_status text,
  last_error text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_snippets_user_id on public.snippets(user_id);
create index if not exists idx_snippets_user_date on public.snippets(user_id, snippet_date);
