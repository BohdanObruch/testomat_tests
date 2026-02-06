from __future__ import annotations

from src.api.controllers.base_controller import BaseController


class TimelineApi(BaseController):
    def list(self, project_id: str, params: dict | None = None) -> dict:
        return self._get(f"/api/{project_id}/timelines", params=params)
