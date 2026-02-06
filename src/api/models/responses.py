from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ListResponse[T](BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: list[T] = Field(default_factory=list)

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]


class ItemResponse[T](BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: T
