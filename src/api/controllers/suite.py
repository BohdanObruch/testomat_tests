from src.api.controllers.base_controller import BaseController
from src.api.models.suite import Suite


class SuiteApi(BaseController):
    def list(self, project_id: str) -> list[Suite]:
        data = self._get(f"/api/{project_id}/suites")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return [Suite.model_validate(item) for item in payload]
        if isinstance(payload, dict) and "data" in payload:
            return [Suite.model_validate(item) for item in payload["data"]]
        return []

    def create(
        self,
        project_id: str,
        title: str,
        description: str | None = None,
    ) -> Suite:
        attributes = {"title": title, "description": description}

        data = self._post(
            f"/api/{project_id}/suites",
            {"data": {"type": "suites", "attributes": attributes}},
        )

        payload = self._extract_data(data)
        return Suite.model_validate(payload)

    def get_by_id(self, project_id: str, suite_id: str) -> Suite:
        data = self._get(f"/api/{project_id}/suites/{suite_id}")
        payload = self._extract_data(data)
        return Suite.model_validate(payload)

    def update(
        self,
        project_id: str,
        suite_id: str,
        title: str | None = None,
        description: str | None = None,
    ) -> Suite:
        attributes = {}
        if title:
            attributes["title"] = title
        if description:
            attributes["description"] = description

        data = self._put(
            f"/api/{project_id}/suites/{suite_id}",
            {"data": {"type": "suites", "attributes": attributes}},
        )
        payload = self._extract_data(data)
        return Suite.model_validate(payload)

    def delete(self, project_id: str, suite_id: str) -> None:
        self._delete(f"/api/{project_id}/suites/{suite_id}")
