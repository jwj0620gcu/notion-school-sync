# Backend (2단계) - FastAPI + Supabase

## 포함 기능

- `FastAPI` API
  - `GET /health`
  - `POST /users/me/sync`
  - `GET /users/me`
  - `PATCH /users/me`
  - `DELETE /users/me`
  - `GET /settings/me`
  - `PUT /settings/me` (API 키 암호화 저장)
  - `GET /dashboard/me`
- `APScheduler` 작업
  - 10분마다: 전체 활성 유저 노션 동기화
  - 매주 월요일 09:00 (Asia/Seoul): 전체 유저 주간 리포트
  - 매월 1일 09:00 (Asia/Seoul): 전체 유저 월간 리포트
- Supabase 테이블 스키마
  - `sql/001_init.sql`
  - `sql/002_analysis.sql`

## 로컬 설정

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.env` 값 입력:

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

`ENCRYPTION_FERNET_KEY` 생성:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 실행

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Supabase SQL 적용

Supabase SQL Editor에서 아래 순서로 실행:

- `backend/sql/001_init.sql`
- `backend/sql/002_analysis.sql`

## 참고 사항

- 2-1 단계는 레거시 `main.py`, `report.py`를 유저별 격리 subprocess로 실행합니다.
- 레거시 실행 시 `USE_SUPABASE_SNIPPETS=1`로 동작하여 스니펫/분석 데이터는 Supabase에 저장됩니다.
- 스케줄러 실행 상태는 `user_state.last_status` 및 타임스탬프로 기록됩니다.
- `SUPABASE_ANON_KEY`가 `sb_publishable_...` 형식일 때 일부 `supabase-py` 버전에서 인증 검증이 실패할 수 있어, 필요 시 `SUPABASE_SERVICE_ROLE_KEY`를 사용합니다.
