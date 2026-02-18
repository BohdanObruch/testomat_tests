import allure
import pytest

from src.api.controllers import (
    AttachmentApi,
    CommentApi,
    JiraIssueApi,
    UserApi,
    UserProjectApi,
)
from src.api.models import CaseModel, Project


@pytest.mark.api
@pytest.mark.regression
class TestMiscEndpoints:
    def test_attachments_list(self, project: Project, created_test: CaseModel, attachment_api: AttachmentApi):
        with allure.step("List attachments for test case"):
            response = attachment_api.list(project.id, params={"test_id": created_test.id})
            assert isinstance(response, (list, dict))

    def test_comments_list(self, project: Project, created_test: CaseModel, comment_api: CommentApi):
        with allure.step("List comments for test case"):
            response = comment_api.list(project.id, params={"test_id": created_test.id})
            assert isinstance(response, dict)

    def test_jira_issues_list(self, project: Project, jira_issue_api: JiraIssueApi):
        with allure.step("List Jira issues for project"):
            response = jira_issue_api.list(project.id)
            assert isinstance(response.data, list)

    def test_users_list(self, project: Project, user_api: UserApi):
        with allure.step("List users for project"):
            response = user_api.list(project.id)
            assert isinstance(response, dict)

    def test_user_project_jira_issues(self, user_project_api: UserProjectApi):
        with allure.step("List Jira issues from user-project endpoint"):
            response = user_project_api.list_jira_issues()
            assert isinstance(response.data, list)
