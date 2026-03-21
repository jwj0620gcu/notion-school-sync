from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

# Always load backend/.env regardless of current working directory.
BACKEND_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)


@dataclass(frozen=True)
class Settings:
    backend_host: str
    backend_port: int
    backend_reload: bool
    cors_allow_origins: list[str]
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    encryption_fernet_key: str
    scheduler_timezone: str


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "y", "on"}


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        backend_host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        backend_port=int(os.getenv("BACKEND_PORT", "8000")),
        backend_reload=_as_bool(os.getenv("BACKEND_RELOAD"), default=True),
        cors_allow_origins=_split_csv(os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000")),
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_anon_key=os.getenv("SUPABASE_ANON_KEY", ""),
        supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
        encryption_fernet_key=os.getenv("ENCRYPTION_FERNET_KEY", ""),
        scheduler_timezone=os.getenv("SCHEDULER_TIMEZONE", "Asia/Seoul"),
    )
