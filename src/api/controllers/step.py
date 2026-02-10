from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models import ItemResponse, ListResponse, Step


class StepApi(BaseController):
    def list(self, project_id: str) -> ListResponse[Step]:
        data = self._get(f"/api/{project_id}/steps")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ListResponse[Step].model_validate({"data": payload})
        return ListResponse[Step].model_validate(payload)

    def count(self, project_id: str) -> dict:
        return self._get(f"/api/{project_id}/steps/count")

    def sync(self, project_id: str) -> dict:
        return self._get(f"/api/{project_id}/steps/sync")

    def get_by_id(self, project_id: str, step_id: str) -> ItemResponse[Step]:
        data = self._get(f"/api/{project_id}/steps/{step_id}")
        payload = self._extract_data(data)
        return ItemResponse[Step].model_validate({"data": payload})

    def create(self, project_id: str, payload: dict) -> ItemResponse[Step]:
        data = self._post(f"/api/{project_id}/steps", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[Step].model_validate({"data": payload})

    def update(self, project_id: str, step_id: str, payload: dict) -> dict:
        return self._patch(f"/api/{project_id}/steps/{step_id}", data=payload)

    def delete(self, project_id: str, step_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/steps/{step_id}")

    def delete_multiple(self, project_id: str, payload: dict) -> dict | None:
        return self._delete(f"/api/{project_id}/steps/delete_multiple", params=payload)

    def clean(self, project_id: str, payload: dict | None = None) -> dict:
        return self._post(f"/api/{project_id}/steps/clean", data=payload or {})

    def merge(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/steps/merge", data=payload)

    def refresh_project(self, project_id: str, payload: dict | None = None) -> dict:
        return self._post(f"/api/{project_id}/steps/refresh_project", data=payload or {})

    def refresh(self, project_id: str, step_id: str, payload: dict | None = None) -> dict:
        return self._post(f"/api/{project_id}/steps/{step_id}/refresh", data=payload or {})
