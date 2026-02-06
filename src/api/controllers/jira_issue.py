from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models import ItemResponse, JiraIssue, ListResponse


class JiraIssueApi(BaseController):
    def list(self, project_id: str) -> ListResponse[JiraIssue]:
        data = self._get(f"/api/{project_id}/jira/issues")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ListResponse[JiraIssue].model_validate({"data": payload})
        return ListResponse[JiraIssue].model_validate(payload)

    def create(self, project_id: str, payload: dict) -> ItemResponse[JiraIssue]:
        data = self._post(f"/api/{project_id}/jira/issues", data=payload)
        payload = self._extract_data(data)
        return ItemResponse[JiraIssue].model_validate({"data": payload})

    def delete(self, project_id: str, issue_id: str) -> dict | None:
        return self._delete(f"/api/{project_id}/jira/issues/{issue_id}")
