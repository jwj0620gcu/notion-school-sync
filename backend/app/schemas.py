from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: str
    email: str | None = None
    display_name: str | None = None


class HealthResponse(BaseModel):
    status: str
    scheduler_running: bool
    timestamp: datetime


class UserResponse(BaseModel):
    id: str
    email: str | None = None
    display_name: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserUpdateRequest(BaseModel):
    display_name: str | None = Field(default=None, max_length=120)


class SettingsUpsertRequest(BaseModel):
    notion_token: str | None = None
    notion_page_id: str | None = None
    school_api_key: str | None = None
    gemini_api_key: str | None = None


class SettingsResponse(BaseModel):
    user_id: str
    notion_page_id: str | None = None
    has_notion_token: bool
    has_school_api_key: bool
    has_gemini_api_key: bool
    updated_at: datetime | None = None


class UserStateResponse(BaseModel):
    user_id: str
    last_notion_check_at: datetime | None = None
    last_notion_sync_at: datetime | None = None
    last_weekly_report_at: datetime | None = None
    last_monthly_report_at: datetime | None = None
    last_status: str | None = None
    last_error: str | None = None
    updated_at: datetime | None = None


class DashboardResponse(BaseModel):
    settings: SettingsResponse
    state: UserStateResponse | None = None
