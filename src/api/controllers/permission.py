from __future__ import annotations

from src.api.controllers.base_controller import BaseController


class PermissionApi(BaseController):
    def list(self, project_id: str) -> dict:
        return self._get(f"/api/{project_id}/permissions")

    def create(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/permissions", data=payload)

    def update(self, project_id: str, permission_id: str, payload: dict) -> dict:
        return self._patch(f"/api/{project_id}/permissions/{permission_id}", data=payload)

    def delete(self, project_id: str, permission_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/permissions/{permission_id}")

    def create_support(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/permissions/support", data=payload)
