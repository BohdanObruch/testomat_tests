from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models import ItemResponse, ListResponse, RunGroup


class RunGroupApi(BaseController):
    def list(self, project_id: str) -> ListResponse[RunGroup]:
        data = self._get(f"/api/{project_id}/rungroups")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ListResponse[RunGroup].model_validate({"data": payload})
        return ListResponse[RunGroup].model_validate(payload)

    def search(self, project_id: str, query: dict) -> dict:
        return self._get(f"/api/{project_id}/rungroups/search", params=query)

    def get_by_id(self, project_id: str, rungroup_id: str) -> ItemResponse[RunGroup]:
        data = self._get(f"/api/{project_id}/rungroups/{rungroup_id}")
        payload = self._extract_data(data)
        return ItemResponse[RunGroup].model_validate({"data": payload})

    def create(self, project_id: str, payload: dict) -> ItemResponse[RunGroup]:
        data = self._post(f"/api/{project_id}/rungroups", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[RunGroup].model_validate({"data": payload})

    def update(self, project_id: str, rungroup_id: str, payload: dict) -> ItemResponse[RunGroup]:
        data = self._put(f"/api/{project_id}/rungroups/{rungroup_id}", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[RunGroup].model_validate({"data": payload})

    def delete(self, project_id: str, rungroup_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/rungroups/{rungroup_id}")

    def delete_multiple(self, project_id: str, payload: dict) -> dict | None:
        return self._delete(f"/api/{project_id}/rungroups/delete_multiple", params=payload)

    def archive(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/rungroups/archive", data=payload)

    def unarchive(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/rungroups/unarchive", data=payload)

    def copy(self, project_id: str, rungroup_id: str, payload: dict | None = None) -> dict:
        return self._post(f"/api/{project_id}/rungroups/{rungroup_id}/copy", data=payload or {})
