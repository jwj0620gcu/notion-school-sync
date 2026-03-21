from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from supabase import Client

from .supabase_client import get_admin_client


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _first_or_none(data: Any) -> dict[str, Any] | None:
    if isinstance(data, list):
        if not data:
            return None
        first = data[0]
        return first if isinstance(first, dict) else None
    if isinstance(data, dict):
        return data
    return None


class UserRepository:
    def __init__(self, client: Client):
        self.client = client

    def upsert(self, *, user_id: str, email: str | None, display_name: str | None = None) -> dict[str, Any]:
        now = utc_now_iso()
        payload = {
            "id": user_id,
            "email": email,
            "display_name": display_name,
            "is_active": True,
            "updated_at": now,
        }
        result = self.client.table("users").upsert(payload, on_conflict="id").execute()
        return _first_or_none(result.data) or payload

    def get(self, user_id: str) -> dict[str, Any] | None:
        result = self.client.table("users").select("*").eq("id", user_id).limit(1).execute()
        return _first_or_none(result.data)

    def update(self, user_id: str, *, display_name: str | None) -> dict[str, Any] | None:
        payload = {"display_name": display_name, "updated_at": utc_now_iso()}
        result = self.client.table("users").update(payload).eq("id", user_id).execute()
        return _first_or_none(result.data)

    def deactivate(self, user_id: str) -> dict[str, Any] | None:
        payload = {"is_active": False, "updated_at": utc_now_iso()}
        result = self.client.table("users").update(payload).eq("id", user_id).execute()
        return _first_or_none(result.data)

    def list_active(self) -> list[dict[str, Any]]:
        result = (
            self.client.table("users")
            .select("*")
            .eq("is_active", True)
            .order("created_at")
            .execute()
        )
        return result.data or []


class SettingsRepository:
    def __init__(self, client: Client):
        self.client = client

    def get(self, user_id: str) -> dict[str, Any] | None:
        result = (
            self.client.table("user_settings")
            .select("*")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        return _first_or_none(result.data)

    def upsert(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        now = utc_now_iso()
        base_payload = {"user_id": user_id, "updated_at": now}
        base_payload.update(payload)
        result = self.client.table("user_settings").upsert(base_payload, on_conflict="user_id").execute()
        return _first_or_none(result.data) or base_payload


class UserStateRepository:
    def __init__(self, client: Client):
        self.client = client

    def get(self, user_id: str) -> dict[str, Any] | None:
        result = self.client.table("user_state").select("*").eq("user_id", user_id).limit(1).execute()
        return _first_or_none(result.data)

    def upsert(self, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        now = utc_now_iso()
        base_payload = {"user_id": user_id, "updated_at": now}
        base_payload.update(payload)
        result = self.client.table("user_state").upsert(base_payload, on_conflict="user_id").execute()
        return _first_or_none(result.data) or base_payload


def get_user_repo() -> UserRepository:
    return UserRepository(get_admin_client())


def get_settings_repo() -> SettingsRepository:
    return SettingsRepository(get_admin_client())


def get_user_state_repo() -> UserStateRepository:
    return UserStateRepository(get_admin_client())
