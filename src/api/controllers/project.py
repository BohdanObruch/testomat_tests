from src.api.controllers.base_controller import BaseController
from src.api.models import Project, ProjectsResponse


class ProjectApi(BaseController):
    def get_all(self) -> ProjectsResponse:
        data = self._get("/api/projects")
        payload = self._extract_data(data)
        if isinstance(payload, list):
            return ProjectsResponse.model_validate({"data": payload})
        return ProjectsResponse.model_validate(payload)

    def get_by_id(self, project_id: str) -> Project:
        data = self._get(f"/api/project/{project_id}")
        payload = self._extract_data(data)
        return Project.model_validate(payload)
