from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class TemplateAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    title: str | None = None
    kind: str | None = None
    body: str | None = None
    framework: str | None = None
    lang: str | None = None
    is_default: bool | None = None
    defect_title: str | None = None
    tags: list[str] | None = None


class Template(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    type: str | None = None
    attributes: TemplateAttributes | None = None
