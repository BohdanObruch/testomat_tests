from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class JiraIssuesAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    jira_urls: list[str] | None = None
    attachables: list[str] | None = None


class JiraIssues(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    attributes: JiraIssuesAttributes | None = None
