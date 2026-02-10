from __future__ import annotations

from src.api.controllers.base_controller import BaseController


class SettingsApi(BaseController):
    def update(self, project_id: str, payload: dict) -> dict:
        return self._put(f"/api/{project_id}/settings", data=payload)
