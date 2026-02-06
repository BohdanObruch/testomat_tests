from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models import ItemResponse, ListResponse, TestRun


class TestRunApi(BaseController):
    def list(self, project_id: str) -> ListResponse[TestRun]:
        data = self._get(f"/api/{project_id}/testruns")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ListResponse[TestRun].model_validate({"data": payload})
        return ListResponse[TestRun].model_validate(payload)

    def get_by_id(self, project_id: str, testrun_id: str) -> ItemResponse[TestRun]:
        data = self._get(f"/api/{project_id}/testruns/{testrun_id}")
        payload = self._extract_data(data)
        return ItemResponse[TestRun].model_validate({"data": payload})

    def create(self, project_id: str, payload: dict) -> ItemResponse[TestRun]:
        data = self._post(f"/api/{project_id}/testruns", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[TestRun].model_validate({"data": payload})

    def update(self, project_id: str, testrun_id: str, payload: dict) -> ItemResponse[TestRun]:
        data = self._put(f"/api/{project_id}/testruns/{testrun_id}", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[TestRun].model_validate({"data": payload})

    def delete(self, project_id: str, testrun_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/testruns/{testrun_id}")

    def add_steps(self, project_id: str, testrun_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/testruns/{testrun_id}/steps", data=payload)
