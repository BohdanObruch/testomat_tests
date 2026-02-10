from __future__ import annotations

from src.api.controllers.base_controller import BaseController
from src.api.models import JiraIssues, ListResponse


class UserProjectApi(BaseController):
    def list_jira_issues(self) -> ListResponse[JiraIssues]:
        data = self._get("/api/user_projects/jiraissues")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ListResponse[JiraIssues].model_validate({"data": payload})
        return ListResponse[JiraIssues].model_validate(payload)
