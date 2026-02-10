from __future__ import annotations

from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class StepAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    title: str | None = None
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "descriprion"),
    )
    kind: str | None = None
    is_snippet: bool | None = None
    keywords: str | list[str] | None = None
    usage_count: int | None = None
    created_at: datetime | None = Field(default=None, alias="created-at")
    updated_at: datetime | None = Field(default=None, alias="updated-at")
    comments_count: int | None = Field(default=None, validation_alias=AliasChoices("comments_count", "comments-count"))


class Step(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    type: str | None = None
    attributes: StepAttributes | None = None
