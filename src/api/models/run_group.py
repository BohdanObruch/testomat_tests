from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RunGroupAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    title: str | None = None
    kind: str | None = None
    emoji: str | None = None
    description: str | None = None
    status: str | None = None
    merge_strategy: str | None = None
    runs_count: int | None = None
    passed: int | None = None
    skipped: int | None = None
    failed: int | None = None
    created_at: datetime | None = Field(default=None, alias="created-at")
    updated_at: datetime | None = Field(default=None, alias="updated-at")
    finished_at: datetime | None = Field(default=None, alias="finished-at")
    is_root: bool | None = Field(default=None, alias="is-root")


class RunGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    attributes: RunGroupAttributes | None = None
    relationships: dict[str, Any] | None = None
