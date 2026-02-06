from src.api.controllers.base_controller import BaseController
from src.api.models import CaseModel


class CaseClient(BaseController):
    def list(self, project_id: str) -> list[CaseModel]:
        data = self._get(f"/api/{project_id}/tests")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return [CaseModel.model_validate(item) for item in payload]
        if isinstance(payload, dict) and "data" in payload:
            return [CaseModel.model_validate(item) for item in payload["data"]]
        return []

    def create(
        self,
        project_id: str,
        suite_id: str,
        title: str,
        description: str | None = None,
        tags: list[str] | None = None,
    ) -> CaseModel:
        attributes: dict = {"title": title, "suite-id": suite_id}
        if description:
            attributes["description"] = description
        if tags:
            attributes["tags"] = tags

        data = self._post(
            f"/api/{project_id}/tests",
            {"data": {"type": "tests", "attributes": attributes}},
        )
        payload = self._extract_data(data)
        return CaseModel.model_validate(payload)

    def get_by_id(self, project_id: str, test_id: str) -> CaseModel:
        data = self._get(f"/api/{project_id}/tests/{test_id}")
        payload = self._extract_data(data)
        return CaseModel.model_validate(payload)

    def update(
        self,
        project_id: str,
        test_id: str,
        title: str | None = None,
        description: str | None = None,
    ) -> CaseModel:
        attributes = {}
        if title:
            attributes["title"] = title
        if description:
            attributes["description"] = description

        data = self._put(
            f"/api/{project_id}/tests/{test_id}",
            {"data": {"type": "tests", "attributes": attributes}},
        )
        payload = self._extract_data(data)
        return CaseModel.model_validate(payload)

    def delete(self, project_id: str, test_id: str) -> None:
        self._delete(f"/api/{project_id}/tests/{test_id}")
