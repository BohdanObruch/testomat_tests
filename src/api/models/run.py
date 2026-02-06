from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class RunAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    title: str | None = None
    status: str | None = None
    multienv: bool | None = None
    checklist: bool | None = None
    access: str | None = None
    to_url: str | None = Field(default=None, validation_alias=AliasChoices("to_url", "to-url"))
    env: list[str] | None = None
    passed: int | None = None
    skipped: int | None = None
    failed: int | None = None
    has_finished: bool | None = Field(default=None, alias="has-finished")
    jira_issues: list[str] | None = Field(default=None, alias="jira-issues")
    created_at: datetime | None = Field(default=None, alias="created-at")
    updated_at: datetime | None = Field(default=None, alias="updated-at")
    finished_at: datetime | None = Field(default=None, alias="finished-at")
    comments_count: int | None = Field(default=None, validation_alias=AliasChoices("comments_count", "comments-count"))


class Run(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    attributes: RunAttributes | None = None
    relationships: dict[str, Any] | None = None
