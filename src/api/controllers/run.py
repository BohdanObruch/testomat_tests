from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models import ItemResponse, ListResponse, Run


class RunApi(BaseController):
    def list(self, project_id: str) -> ListResponse[Run]:
        data = self._get(f"/api/{project_id}/runs")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ListResponse[Run].model_validate({"data": payload})
        return ListResponse[Run].model_validate(payload)

    def count(self, project_id: str) -> dict:
        return self._get(f"/api/{project_id}/runs/count")

    def dashboard(self, project_id: str) -> dict:
        return self._get(f"/api/{project_id}/runs/dashboard")

    def download(self, project_id: str, params: dict | None = None) -> dict:
        return self._get(f"/api/{project_id}/runs/download", params=params)

    def get_by_id(self, project_id: str, run_id: str) -> ItemResponse[Run]:
        data = self._get(f"/api/{project_id}/runs/{run_id}")
        payload = self._extract_data(data)
        return ItemResponse[Run].model_validate({"data": payload})

    def create(self, project_id: str, payload: dict) -> ItemResponse[Run]:
        data = self._post(f"/api/{project_id}/runs", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[Run].model_validate({"data": payload})

    def update(self, project_id: str, run_id: str, payload: dict) -> ItemResponse[Run]:
        data = self._put(f"/api/{project_id}/runs/{run_id}", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[Run].model_validate({"data": payload})

    def delete(self, project_id: str, run_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/runs/{run_id}")

    def delete_multiple(self, project_id: str, payload: dict) -> dict | None:
        return self._delete(f"/api/{project_id}/runs/delete_multiple", params=payload)

    def merge(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/runs/merge", data=payload)

    def configuration_preview(self, project_id: str, run_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/runs/{run_id}/configuration_preview", data=payload)

    def email(self, project_id: str, run_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/runs/{run_id}/email", data=payload)

    def plan(self, project_id: str, run_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/runs/{run_id}/plan", data=payload)

    def reconfigure(self, project_id: str, run_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/runs/{run_id}/reconfigure", data=payload)

    def relaunch(self, project_id: str, run_id: str, payload: dict | None = None) -> dict:
        return self._post(f"/api/{project_id}/runs/{run_id}/relaunch", data=payload or {})

    def relaunch_copy(self, project_id: str, run_id: str, payload: dict | None = None) -> dict:
        return self._post(f"/api/{project_id}/runs/{run_id}/relaunch_copy", data=payload or {})

    def entries(self, project_id: str, run_id: str) -> dict:
        return self._get(f"/api/{project_id}/runs/{run_id}/entries")

    def publish(self, project_id: str, run_id: str) -> dict:
        return self._get(f"/api/{project_id}/runs/{run_id}/publish")

    def archives(self, project_id: str) -> dict:
        return self._get(f"/api/{project_id}/runs/archives")
