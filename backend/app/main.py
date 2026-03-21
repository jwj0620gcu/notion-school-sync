from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routes.dashboard import router as dashboard_router
from .routes.settings import router as settings_router
from .routes.users import router as users_router
from .scheduler import create_scheduler
from .schemas import HealthResponse

settings = get_settings()
scheduler, _runner = create_scheduler(settings.scheduler_timezone)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)


app = FastAPI(
    title="Notion School Sync Backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins or ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(settings_router)
app.include_router(dashboard_router)


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        scheduler_running=scheduler.running,
        timestamp=datetime.now(timezone.utc),
    )


@app.post("/scheduler/run/notion-sync")
def run_notion_sync_now():
    scheduler.add_job(_runner.run_notion_sync)
    return {"queued": True}


@app.post("/scheduler/run/weekly-report")
def run_weekly_report_now():
    scheduler.add_job(_runner.run_weekly_report)
    return {"queued": True}


@app.post("/scheduler/run/monthly-report")
def run_monthly_report_now():
    scheduler.add_job(_runner.run_monthly_report)
    return {"queued": True}
