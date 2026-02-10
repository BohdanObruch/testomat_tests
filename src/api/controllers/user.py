from __future__ import annotations

from src.api.controllers.base_controller import BaseController


class UserApi(BaseController):
    def list(self, project_id: str) -> dict:
        return self._get(f"/api/{project_id}/users")

    def get_by_id(self, project_id: str, user_id: str) -> dict:
        return self._get(f"/api/{project_id}/users/{user_id}")
