from __future__ import annotations

from src.api.controllers.base_controller import BaseController


class AttachmentApi(BaseController):
    def list(self, project_id: str, params: dict | None = None) -> dict:
        return self._get(f"/api/{project_id}/attachments", params=params)

    def create(self, project_id: str, payload: dict) -> dict:
        return self._post(f"/api/{project_id}/attachments", data=payload)

    def delete(self, project_id: str, attachment_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/attachments/{attachment_id}")

    def restore(self, project_id: str, attachment_id: str) -> dict:
        return self._post(f"/api/{project_id}/attachments/{attachment_id}/restore")
