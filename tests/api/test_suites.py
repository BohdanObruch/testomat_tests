import pytest
from faker import Faker

from src.api.controllers import SuiteApi
from src.api.models import Project, Suite

fake = Faker()


@pytest.mark.api
class TestSuites:
    def test_list_suites(self, project: Project, suite_api: SuiteApi):
        suites = suite_api.list(project.id)
        assert isinstance(suites, list)

    def test_update_suite(self, project: Project, suite_api: SuiteApi, created_suite: Suite):
        updated = suite_api.update(
            project_id=project.id,
            suite_id=created_suite.id,
            title=fake.sentence(),
        )
        assert updated.id == created_suite.id
