from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status

from ..auth import get_current_user
from ..repositories import UserRepository, get_user_repo
from ..schemas import CurrentUser, UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


def _to_user_response(record: dict) -> UserResponse:
    return UserResponse(
        id=str(record.get("id")),
        email=record.get("email"),
        display_name=record.get("display_name"),
        is_active=bool(record.get("is_active", True)),
        created_at=record.get("created_at"),
        updated_at=record.get("updated_at"),
    )


@router.post("/me/sync", response_model=UserResponse)
def sync_current_user(
    current_user: CurrentUser = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
):
    try:
        record = user_repo.upsert(
            user_id=current_user.id,
            email=current_user.email,
            display_name=current_user.display_name,
        )
        return _to_user_response(record)
    except Exception as exc:
        logger.exception("sync_current_user failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"users/me/sync failed: {exc}",
        ) from exc


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: CurrentUser = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
):
    try:
        record = user_repo.get(current_user.id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return _to_user_response(record)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("get_me failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"users/me failed: {exc}",
        ) from exc


@router.patch("/me", response_model=UserResponse)
def update_me(
    body: UserUpdateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
):
    try:
        record = user_repo.update(current_user.id, display_name=body.display_name)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return _to_user_response(record)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("update_me failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"users/me update failed: {exc}",
        ) from exc


@router.delete("/me", response_model=UserResponse)
def deactivate_me(
    current_user: CurrentUser = Depends(get_current_user),
    user_repo: UserRepository = Depends(get_user_repo),
):
    try:
        record = user_repo.deactivate(current_user.id)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return _to_user_response(record)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("deactivate_me failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"users/me deactivate failed: {exc}",
        ) from exc
