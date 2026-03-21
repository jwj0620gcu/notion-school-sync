from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status

from ..auth import get_current_user
from ..repositories import (
    SettingsRepository,
    UserStateRepository,
    get_settings_repo,
    get_user_state_repo,
)
from ..schemas import CurrentUser, DashboardResponse, SettingsResponse, UserStateResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
logger = logging.getLogger(__name__)


def _to_settings_response(user_id: str, record: dict | None) -> SettingsResponse:
    record = record or {}
    return SettingsResponse(
        user_id=user_id,
        notion_page_id=record.get("notion_page_id"),
        has_notion_token=bool(record.get("notion_token_enc")),
        has_school_api_key=bool(record.get("school_api_key_enc")),
        has_gemini_api_key=bool(record.get("gemini_api_key_enc")),
        updated_at=record.get("updated_at"),
    )


def _to_state_response(user_id: str, record: dict | None) -> UserStateResponse | None:
    if not record:
        return None
    return UserStateResponse(
        user_id=user_id,
        last_notion_check_at=record.get("last_notion_check_at"),
        last_notion_sync_at=record.get("last_notion_sync_at"),
        last_weekly_report_at=record.get("last_weekly_report_at"),
        last_monthly_report_at=record.get("last_monthly_report_at"),
        last_status=record.get("last_status"),
        last_error=record.get("last_error"),
        updated_at=record.get("updated_at"),
    )


@router.get("/me", response_model=DashboardResponse)
def get_my_dashboard(
    current_user: CurrentUser = Depends(get_current_user),
    settings_repo: SettingsRepository = Depends(get_settings_repo),
    state_repo: UserStateRepository = Depends(get_user_state_repo),
):
    try:
        settings_row = settings_repo.get(current_user.id)
        state_row = state_repo.get(current_user.id)
        return DashboardResponse(
            settings=_to_settings_response(current_user.id, settings_row),
            state=_to_state_response(current_user.id, state_row),
        )
    except Exception as exc:
        logger.exception("get_my_dashboard failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"dashboard/me failed: {exc}",
        ) from exc
