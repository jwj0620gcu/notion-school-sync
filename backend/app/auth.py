from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .schemas import CurrentUser
from .supabase_client import get_auth_client

bearer_scheme = HTTPBearer(auto_error=False)


def _read_attr(data: object, field: str) -> str | None:
    if isinstance(data, dict):
        value = data.get(field)
        return str(value) if value is not None else None
    value = getattr(data, field, None)
    return str(value) if value is not None else None


def _parse_user(user_obj: object) -> CurrentUser:
    user_id = _read_attr(user_obj, "id")
    email = _read_attr(user_obj, "email")
    display_name = _read_attr(user_obj, "display_name")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Supabase access token.",
        )
    return CurrentUser(id=user_id, email=email, display_name=display_name)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization token.",
        )

    try:
        token = credentials.credentials
        supabase = get_auth_client()
        response = supabase.auth.get_user(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {exc}",
        ) from exc

    user_obj = getattr(response, "user", None)
    if user_obj is None and isinstance(response, dict):
        user_obj = response.get("user")

    return _parse_user(user_obj)
