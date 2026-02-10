from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JiraIssueAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    url: str | None = None
    attachables: list[str] | None = None
    created_at: datetime | None = Field(default=None, alias="created-at")
    updated_at: datetime | None = Field(default=None, alias="updated-at")


class JiraIssue(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    attributes: JiraIssueAttributes | None = None
