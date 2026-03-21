# Web (1~2단계) - Next.js UI

## 범위

- Google OAuth 로그인 (Supabase Auth)
- API 키 입력 페이지 (`/settings`)
- 대시보드 (`/dashboard`)
- 백엔드 API 연동 (암호화 설정 저장, 유저 상태 조회)

## 로컬 실행

```bash
cd web
cp .env.example .env.local
npm install
npm run dev
```

## 필수 환경변수

```bash
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_BACKEND_API_URL=http://localhost:8000
```

## Supabase + Google OAuth 설정 (필수)

1. Supabase 프로젝트 생성
2. Google Cloud Console에서 OAuth Client ID 생성 (웹 애플리케이션)
3. Google OAuth Redirect URI 등록
   - `https://<your-project-ref>.supabase.co/auth/v1/callback`
4. Supabase `Authentication > Providers > Google`에서 Client ID/Secret 입력
5. Supabase `Authentication > URL Configuration`
   - Site URL: `http://localhost:3000` (개발), `https://<your-vercel-domain>` (배포)
   - Redirect URLs:
     - `http://localhost:3000/auth/callback`
     - `https://<your-vercel-domain>/auth/callback`
6. Supabase URL, anon/publishable 키를 `.env.local`에 반영

## 백엔드 선행 조건 (2단계)

`/settings`, `/dashboard` 테스트 전 아래 백엔드 API가 실행 중이어야 합니다.

- `POST /users/me/sync`
- `GET /settings/me`
- `PUT /settings/me`
- `GET /dashboard/me`

`NEXT_PUBLIC_BACKEND_API_URL`에 FastAPI 주소를 넣고 테스트하세요.

## Vercel 배포 설정

1. Vercel에서 `web` 디렉터리를 프로젝트로 연결
2. 동일한 환경변수 등록
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_APP_URL` (Vercel 도메인)
   - `NEXT_PUBLIC_BACKEND_API_URL` (배포된 FastAPI 주소)
3. 환경변수 변경 후 재배포
