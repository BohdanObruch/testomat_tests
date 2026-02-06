from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models import ItemResponse, ListResponse, Plan


class PlanApi(BaseController):
    def list(self, project_id: str) -> ListResponse[Plan]:
        data = self._get(f"/api/{project_id}/plans")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ListResponse[Plan].model_validate({"data": payload})
        return ListResponse[Plan].model_validate(payload)

    def count(self, project_id: str) -> dict:
        return self._get(f"/api/{project_id}/plans/count")

    def get_by_id(self, project_id: str, plan_id: str) -> ItemResponse[Plan]:
        data = self._get(f"/api/{project_id}/plans/{plan_id}")
        payload = self._extract_data(data)
        return ItemResponse[Plan].model_validate({"data": payload})

    def create(self, project_id: str, payload: dict) -> ItemResponse[Plan]:
        data = self._post(f"/api/{project_id}/plans", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[Plan].model_validate({"data": payload})

    def update(self, project_id: str, plan_id: str, payload: dict) -> ItemResponse[Plan]:
        data = self._put(f"/api/{project_id}/plans/{plan_id}", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[Plan].model_validate({"data": payload})

    def delete(self, project_id: str, plan_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/plans/{plan_id}")

    def validate(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/plans/validate", data=payload)
