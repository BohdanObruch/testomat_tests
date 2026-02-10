from __future__ import annotations

from src.api.controllers.base_controller import BaseController


class CommentApi(BaseController):
    def list(self, project_id: str, params: dict | None = None) -> dict:
        return self._get(f"/api/{project_id}/comments", params=params)

    def create(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/comments", data=payload)

    def update(self, project_id: str, comment_id: str, payload: dict) -> dict:
        return self._patch(f"/api/{project_id}/comments/{comment_id}", data=payload)

    def delete(self, project_id: str, comment_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/comments/{comment_id}")
