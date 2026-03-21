# Web (Step 1-2) - Next.js UI

## Scope

- Google OAuth login (Supabase Auth)
- API key input page (`/settings`)
- Dashboard (`/dashboard`)
- Backend API integration for encrypted settings save and user state

## Local Run

```bash
cd web
cp .env.example .env.local
npm install
npm run dev
```

## Required Environment Variables

```bash
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:8000
```

## Supabase + Google OAuth Setup (Required)

1. Create project in Supabase.
2. In Google Cloud Console, create OAuth Client ID (Web app).
3. In Google OAuth Authorized redirect URI, add:
   - `https://<your-project-ref>.supabase.co/auth/v1/callback`
4. In Supabase `Authentication > Providers > Google`, set Google Client ID/Secret.
5. In Supabase `Authentication > URL Configuration`:
   - Site URL: `http://localhost:3000` (dev) and your Vercel URL (prod)
   - Redirect URLs:
     - `http://localhost:3000/auth/callback`
     - `https://<your-vercel-domain>/auth/callback`
6. Copy project URL and anon key to `.env.local`.

## Backend Required (Step 2)

The UI now calls these backend APIs:

- `POST /users/me/sync`
- `GET /settings/me`
- `PUT /settings/me`
- `GET /dashboard/me`

Set `NEXT_PUBLIC_BACKEND_API_URL` to your FastAPI URL and run backend before testing `/settings` and `/dashboard`.

## Vercel Setup (Required for deploy)

1. Import this `web` directory as a Vercel project.
2. Add the same environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_APP_URL` (set to your Vercel URL)
   - `NEXT_PUBLIC_BACKEND_API_URL` (FastAPI URL, can be placeholder for now)
3. Redeploy after env updates.
