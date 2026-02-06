import pytest
from faker import Faker

from src.api.client import ApiClient
from src.api.controllers import CaseClient
from src.api.models import CaseModel, Project, ProjectsResponse

fake = Faker()


@pytest.mark.api
class TestAuthentication:
    def test_login_with_valid_token(self, api_client: ApiClient):
        jwt_token = api_client._authenticate()

        assert isinstance(jwt_token, str)
        assert jwt_token

    def test_jwt_token_is_cached(self, api_client: ApiClient):
        first_token = api_client._authenticate()
        second_token = api_client._authenticate()

        assert first_token == second_token


@pytest.mark.api
class TestProjects:
    def test_get_projects_returns_response(self, api_client: ApiClient):
        response = api_client.get_projects()

        assert isinstance(response, ProjectsResponse)

    def test_get_projects_returns_list_of_projects(self, api_client: ApiClient):
        response = api_client.get_projects()

        assert isinstance(response.data, list)
        if response:
            assert isinstance(response[0], Project)

    def test_project_has_required_attributes(self, api_client: ApiClient):
        response = api_client.get_projects()

        if response:
            project = response[0]
            assert project.id
            assert project.type == "project"
            assert project.title
            assert project.status


class TestProjectTests:
    def test_list_project_tests(self, project: Project, test_api: CaseClient):
        tests = test_api.list(project.id)
        assert isinstance(tests, list)

    def test_update_project_test(self, project: Project, test_api: CaseClient, created_test: CaseModel):
        updated = test_api.update(
            project_id=project.id,
            test_id=created_test.id,
            title=fake.sentence(),
        )
        assert updated.id == created_test.id
