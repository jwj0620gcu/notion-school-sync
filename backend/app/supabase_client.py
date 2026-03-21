from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from .config import get_settings


def _build_client(url: str, key: str) -> Client:
    if not url or not key:
        raise RuntimeError("SUPABASE_URL / SUPABASE key is missing.")
    return create_client(url, key)


@lru_cache(maxsize=1)
def get_auth_client() -> Client:
    settings = get_settings()
    # supabase-py auth flow may reject new publishable keys (sb_publishable_...).
    # In backend-only context, fallback to service_role for token verification.
    key = settings.supabase_anon_key
    if key.startswith("sb_") and settings.supabase_service_role_key:
        key = settings.supabase_service_role_key
    return _build_client(settings.supabase_url, key)


@lru_cache(maxsize=1)
def get_admin_client() -> Client:
    settings = get_settings()
    return _build_client(settings.supabase_url, settings.supabase_service_role_key)
