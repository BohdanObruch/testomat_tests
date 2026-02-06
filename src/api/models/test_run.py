from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TestRunAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    title: str | None = None
    status: str | None = None
    message: str | None = None
    stack: str | None = None
    steps: dict | None = None
    run_time: float | None = Field(default=None, alias="run_time")
    created_at: datetime | None = Field(default=None, alias="created-at")
    updated_at: datetime | None = Field(default=None, alias="updated-at")
    finished_at: datetime | None = Field(default=None, alias="finished-at")


class TestRun(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    attributes: TestRunAttributes | None = None
