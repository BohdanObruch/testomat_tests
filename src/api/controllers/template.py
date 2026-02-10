from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models import ItemResponse, ListResponse, Template


class TemplateApi(BaseController):
    def list(self, project_id: str, kind: str | None = None) -> ListResponse[Template]:
        data = self._get(f"/api/{project_id}/templates", params={"kind": kind})
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ListResponse[Template].model_validate({"data": payload})
        return ListResponse[Template].model_validate(payload)

    def get_default_for_kind(self, project_id: str, kind: str) -> dict:
        return self._get(f"/api/{project_id}/templates/kind/{kind}")

    def get_by_id(self, project_id: str, template_id: str, model: str | None = None) -> ItemResponse[Template]:
        data = self._get(
            f"/api/{project_id}/templates/{template_id}",
            params={"model": model},
        )
        payload = self._extract_data(data)
        return ItemResponse[Template].model_validate({"data": payload})

    def create(self, project_id: str, payload: dict) -> ItemResponse[Template]:
        data = self._post(f"/api/{project_id}/templates", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[Template].model_validate({"data": payload})

    def update(self, project_id: str, template_id: str, payload: dict) -> ItemResponse[Template]:
        data = self._put(f"/api/{project_id}/templates/{template_id}", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[Template].model_validate({"data": payload})

    def delete(self, project_id: str, template_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/templates/{template_id}")

    def refresh(self, project_id: str) -> dict:
        return self._post(f"/api/{project_id}/templates/refresh")
