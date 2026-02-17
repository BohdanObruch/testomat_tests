import allure
import httpx
import pytest
from faker import Faker

from src.api.client import ApiClient
from src.api.controllers import (
    AnalyticsApi,
    AttachmentApi,
    CaseClient,
    CommentApi,
    JiraIssueApi,
    PermissionApi,
    PlanApi,
    ProjectApi,
    RunApi,
    RunGroupApi,
    SettingsApi,
    StepApi,
    SuiteApi,
    TemplateApi,
    TestRunApi,
    TimelineApi,
    UserApi,
    UserProjectApi,
)
from src.api.models import CaseModel, Plan, Project, Run, RunGroup, Step, Suite, Template, TestRun
from tests.fixtures.config import Config

fake = Faker()


@pytest.fixture(scope="session")
def auth_token(configs: Config) -> str:
    """Single authentication token shared across all controllers."""
    with allure.step("Authenticate test session token"):
        response = httpx.post(
            f"{configs.app_base_url}/api/login",
            json={"api_token": configs.testomat_token},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["jwt"]


@pytest.fixture(scope="session")
def project_api(configs: Config, auth_token: str) -> ProjectApi:
    controller = ProjectApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def suite_api(configs: Config, auth_token: str) -> SuiteApi:
    controller = SuiteApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def test_api(configs: Config, auth_token: str) -> CaseClient:
    controller = CaseClient(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )
    yield controller


@pytest.fixture(scope="session")
def api_client(configs: Config) -> ApiClient:
    return ApiClient(base_url=configs.app_base_url, api_token=configs.testomat_token)


@pytest.fixture(scope="session")
def analytics_api(configs: Config, auth_token: str) -> AnalyticsApi:
    return AnalyticsApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def attachment_api(configs: Config, auth_token: str) -> AttachmentApi:
    return AttachmentApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def comment_api(configs: Config, auth_token: str) -> CommentApi:
    return CommentApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def jira_issue_api(configs: Config, auth_token: str) -> JiraIssueApi:
    return JiraIssueApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def permission_api(configs: Config, auth_token: str) -> PermissionApi:
    return PermissionApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def plan_api(configs: Config, auth_token: str) -> PlanApi:
    return PlanApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def rungroup_api(configs: Config, auth_token: str) -> RunGroupApi:
    return RunGroupApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def run_api(configs: Config, auth_token: str) -> RunApi:
    return RunApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def settings_api(configs: Config, auth_token: str) -> SettingsApi:
    return SettingsApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def step_api(configs: Config, auth_token: str) -> StepApi:
    return StepApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def template_api(configs: Config, auth_token: str) -> TemplateApi:
    return TemplateApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def testrun_api(configs: Config, auth_token: str) -> TestRunApi:
    return TestRunApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def timeline_api(configs: Config, auth_token: str) -> TimelineApi:
    return TimelineApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def user_api(configs: Config, auth_token: str) -> UserApi:
    return UserApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="session")
def user_project_api(configs: Config, auth_token: str) -> UserProjectApi:
    return UserProjectApi(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
        jwt_token=auth_token,
    )


@pytest.fixture(scope="function")
def project(project_api: ProjectApi) -> Project:
    """Get the first available project as a precondition."""
    with allure.step("Get first available project"):
        projects = project_api.get_all()
        return projects[0]


@pytest.fixture(scope="function")
def created_suite(project: Project, suite_api: SuiteApi) -> Suite:
    with allure.step("Create suite fixture"):
        created = suite_api.create(project_id=project.id, title=fake.sentence())
    yield created
    with allure.step("Delete suite fixture"):
        suite_api.delete(project.id, created.id)


@pytest.fixture(scope="function")
def created_test(
    project: Project,
    created_suite: Suite,
    test_api: CaseClient,
) -> CaseModel:
    with allure.step("Create test case fixture"):
        tag = f"plan_{fake.word()}"
        test_case = test_api.create(
            project_id=project.id,
            suite_id=created_suite.id,
            title=fake.sentence(),
            tags=[tag],
        )
    yield test_case
    with allure.step("Delete test case fixture"):
        test_api.delete(project.id, test_case.id)


@pytest.fixture(scope="function")
def created_step(project: Project, step_api: StepApi) -> Step:
    with allure.step("Create step fixture"):
        payload = {"data": {"type": "steps", "attributes": {"title": fake.sentence()}}}
        created = step_api.create(project.id, payload).data
    yield created
    with allure.step("Delete step fixture"):
        step_api.delete(project.id, created.id)


@pytest.fixture(scope="function")
def created_rungroup(project: Project, rungroup_api: RunGroupApi) -> RunGroup:
    with allure.step("Create run group fixture"):
        payload = {
            "data": {
                "type": "rungroups",
                "attributes": {
                    "title": fake.sentence(),
                    "kind": "build",
                    "merge_strategy": "realistic",
                },
            }
        }
        created = rungroup_api.create(project.id, payload).data
    yield created
    with allure.step("Delete run group fixture"):
        rungroup_api.delete(project.id, created.id)


@pytest.fixture(scope="function")
def created_run(project: Project, created_rungroup: RunGroup, run_api: RunApi) -> Run:
    with allure.step("Create run fixture"):
        payload = {
            "data": {
                "type": "runs",
                "attributes": {
                    "title": fake.sentence(),
                    "rungroup_id": created_rungroup.id,
                },
            }
        }
        created = run_api.create(project.id, payload).data
    yield created
    with allure.step("Delete run fixture"):
        run_api.delete(project.id, created.id)


@pytest.fixture(scope="function")
def created_testrun(
    project: Project,
    created_run: Run,
    created_test: CaseModel,
    testrun_api: TestRunApi,
) -> TestRun:
    with allure.step("Create test run fixture"):
        payload = {
            "data": {
                "type": "testruns",
                "attributes": {
                    "run_id": created_run.id,
                    "test_id": created_test.id,
                    "status": "passed",
                },
            }
        }
        created = testrun_api.create(project.id, payload).data
    yield created
    with allure.step("Delete test run fixture"):
        testrun_api.delete(project.id, created.id)


@pytest.fixture(scope="function")
def created_template(project: Project, template_api: TemplateApi) -> Template:
    with allure.step("Create template fixture"):
        payload = {
            "data": {
                "type": "templates",
                "attributes": {
                    "title": fake.sentence(),
                    "kind": "test",
                    "body": "### Steps",
                },
            }
        }
        created = template_api.create(project.id, payload).data
    yield created
    with allure.step("Delete template fixture"):
        template_api.delete(project.id, created.id)


@pytest.fixture(scope="function")
def created_plan(project: Project, created_suite: Suite, plan_api: PlanApi) -> Plan:
    with allure.step("Create plan fixture"):
        payload = {
            "data": {
                "type": "plans",
                "attributes": {
                    "title": fake.sentence(),
                    "kind": "manual",
                    "test-plan": {"suites": [created_suite.id]},
                },
            }
        }
        created = plan_api.create(project.id, payload=payload).data
    yield created
    with allure.step("Delete plan fixture"):
        plan_api.delete(project.id, created.id)
