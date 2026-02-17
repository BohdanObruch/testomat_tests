import allure
import pytest
from faker import Faker

from src.api.controllers import CaseClient, SuiteApi
from src.api.models import CaseModel, Project, Suite

fake = Faker()


@pytest.mark.smoke
@pytest.mark.api
def test_create_suite_roundtrip(project: Project, suite_api: SuiteApi):
    with allure.step("Create suite and verify roundtrip"):
        suite_name = fake.sentence()
        created = suite_api.create(project_id=project.id, title=suite_name, description=fake.paragraph())
        fetched = suite_api.get_by_id(project.id, created.id)

        assert created.id == fetched.id
        assert fetched.attributes.title == suite_name

    with allure.step("Cleanup created suite"):
        suite_api.delete(project.id, created.id)


@pytest.mark.smoke
@pytest.mark.api
def test_create_test_case_roundtrip(project: Project, suite_api: SuiteApi, test_api: CaseClient):
    with allure.step("Create suite and test case"):
        suite: Suite = suite_api.create(project_id=project.id, title=fake.sentence())
        test_title = fake.sentence()
        created: CaseModel = test_api.create(
            project_id=project.id,
            suite_id=suite.id,
            title=test_title,
            description=fake.paragraph(),
        )

    with allure.step("Fetch test case and verify values"):
        fetched = test_api.get_by_id(project.id, created.id)
        assert fetched.id == created.id
        assert fetched.title == test_title

    with allure.step("Cleanup created test case and suite"):
        test_api.delete(project.id, created.id)
        suite_api.delete(project.id, suite.id)
