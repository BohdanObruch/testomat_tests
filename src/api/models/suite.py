from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class SuiteAttributes(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    suite_id: str | None = Field(default=None, alias="suite-id")
    title: str | None = None
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "descriprion"),
    )
    code: str | None = None
    file: str | None = None
    fullpath: str | None = None
    file_type: str | None = Field(default=None, alias="file-type")
    to_url: str | None = Field(default=None, validation_alias=AliasChoices("to_url", "to-url"))
    tags: list[str] | None = None
    test_count: int | None = Field(default=None, alias="test-count")
    tests: list[str] | None = None
    children: list[str] | None = None
    created_at: datetime | None = Field(default=None, alias="created-at")
    updated_at: datetime | None = Field(default=None, alias="updated-at")
    comments_count: int | None = Field(default=None, validation_alias=AliasChoices("comments_count", "comments-count"))


class Suite(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str | None = None
    type: str | None = None
    attributes: SuiteAttributes | None = None
    relationships: dict[str, Any] | None = None
