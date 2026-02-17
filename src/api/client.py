import allure
import httpx

from src.api.models.project import ProjectsResponse


class ApiClient:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self._client = httpx.Client(timeout=30)
        self._jwt_token: str | None = None

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}{endpoint}"

    def _authenticate(self) -> str:
        if self._jwt_token:
            return self._jwt_token

        with allure.step("Authenticate ApiClient"):
            response = self._client.post(
                self._url("/api/login"),
                json={"api_token": self.api_token},
            )
            response.raise_for_status()
            self._jwt_token = response.json()["jwt"]
            return self._jwt_token

    def _get_auth_headers(self) -> dict[str, str]:
        jwt = self._authenticate()
        return {"Authorization": f"Bearer {jwt}"}

    def get_projects(self) -> ProjectsResponse:
        with allure.step("GET /api/projects"):
            response = self._client.get(
                self._url("/api/projects"),
                headers=self._get_auth_headers(),
            )
            response.raise_for_status()
            return ProjectsResponse.model_validate(response.json())
