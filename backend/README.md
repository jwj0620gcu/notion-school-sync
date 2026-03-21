# Backend (Step 2) - FastAPI + Supabase

## What is included

- `FastAPI` APIs
  - `GET /health`
  - `POST /users/me/sync`
  - `GET /users/me`
  - `PATCH /users/me`
  - `DELETE /users/me`
  - `GET /settings/me`
  - `PUT /settings/me` (API key encryption)
  - `GET /dashboard/me`
- `APScheduler` jobs
  - every 10 minutes: notion sync loop for all active users
  - monday 09:00 (Asia/Seoul): weekly report loop for all active users
  - day 1 09:00 (Asia/Seoul): monthly report loop for all active users
- Supabase table schema at `sql/001_init.sql`

## Setup

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Fill `.env`:

```bash
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_RELOAD=true
CORS_ALLOW_ORIGINS=http://localhost:3000

SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
ENCRYPTION_FERNET_KEY=
```

Note:
- If `SUPABASE_ANON_KEY` is a new publishable key format (`sb_publishable_...`), backend auth verification can fail on some supabase-py versions.
- In this backend, auth verification falls back to `SUPABASE_SERVICE_ROLE_KEY` automatically when needed.

Generate `ENCRYPTION_FERNET_KEY`:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Supabase SQL

Open Supabase SQL Editor and run:

- `backend/sql/001_init.sql`
- `backend/sql/002_analysis.sql`

## Notes

- Step 2-1 runs legacy `main.py` and `report.py` in isolated subprocesses per user.
- Legacy scripts run with `USE_SUPABASE_SNIPPETS=1`, so snippet/analysis data is persisted in Supabase (no local SQLite dependency for scheduler/report flow).
- Scheduler status is written to `user_state.last_status` and timestamps are updated per job.
