import pytest
from faker import Faker

from src.api.controllers import CaseClient, SuiteApi
from src.api.models import CaseModel, Project, Suite

fake = Faker()


@pytest.mark.smoke
@pytest.mark.api
def test_create_suite_roundtrip(project: Project, suite_api: SuiteApi):
    suite_name = fake.sentence()
    created = suite_api.create(project_id=project.id, title=suite_name, description=fake.paragraph())

    fetched = suite_api.get_by_id(project.id, created.id)

    assert created.id == fetched.id
    assert fetched.attributes.title == suite_name

    suite_api.delete(project.id, created.id)


@pytest.mark.smoke
@pytest.mark.api
def test_create_test_case_roundtrip(project: Project, suite_api: SuiteApi, test_api: CaseClient):
    suite: Suite = suite_api.create(project_id=project.id, title=fake.sentence())

    test_title = fake.sentence()
    created: CaseModel = test_api.create(
        project_id=project.id,
        suite_id=suite.id,
        title=test_title,
        description=fake.paragraph(),
    )

    fetched = test_api.get_by_id(project.id, created.id)

    assert fetched.id == created.id
    assert fetched.title == test_title

    test_api.delete(project.id, created.id)
    suite_api.delete(project.id, suite.id)
