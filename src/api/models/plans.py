from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PlanAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    tests_ids: list[str] | None = Field(default=None, alias="tests-ids")
    jira_issues: list[str] | None = Field(default=None, alias="jira-issues")
    created_at: datetime | None = Field(default=None, alias="created-at")


class Plan(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    attributes: PlanAttributes | None = None
