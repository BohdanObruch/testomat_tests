import pytest

from src.api.controllers import AnalyticsApi
from src.api.models import Project
from src.api.utils import extract_first_id


@pytest.mark.api
class TestAnalytics:
    def test_labels_and_label_detail(self, project: Project, analytics_api: AnalyticsApi):
        labels = analytics_api.get_labels_stats(project.id)
        assert isinstance(labels, dict)

        label_id = extract_first_id(labels)
        if label_id:
            detail = analytics_api.get_label_detail(project.id, label_id)
            assert isinstance(detail, dict)

    def test_jira_and_issue_detail(self, project: Project, analytics_api: AnalyticsApi):
        jira = analytics_api.get_jira_stats(project.id)
        assert isinstance(jira, dict)

        issue_id = extract_first_id(jira)
        if issue_id:
            detail = analytics_api.get_jira_issue(project.id, issue_id)
            assert isinstance(detail, dict)

    def test_tags_and_tag_detail(self, project: Project, analytics_api: AnalyticsApi):
        tags = analytics_api.get_tags_stats(project.id)
        assert isinstance(tags, dict)

        tag_id = extract_first_id(tags)
        if tag_id:
            detail = analytics_api.get_tag_detail(project.id, tag_id)
            assert isinstance(detail, dict)

    def test_runenvs_and_detail(self, project: Project, analytics_api: AnalyticsApi):
        envs = analytics_api.get_runenvs_stats(project.id)
        assert isinstance(envs, dict)

        env_id = extract_first_id(envs)
        if env_id:
            detail = analytics_api.get_runenv_detail(project.id, env_id)
            assert isinstance(detail, dict)

    def test_tests_analytics(self, project: Project, analytics_api: AnalyticsApi):
        assert isinstance(analytics_api.get_automation(project.id), dict)
        assert isinstance(analytics_api.get_counters(project.id), dict)
        assert isinstance(analytics_api.get_failing(project.id), dict)
        assert isinstance(analytics_api.get_failures(project.id), dict)
        assert isinstance(analytics_api.get_flaky(project.id), dict)
        assert isinstance(analytics_api.get_issues(project.id), dict)
        assert isinstance(analytics_api.get_pending(project.id), dict)
        assert isinstance(analytics_api.get_slow(project.id), dict)

    def test_issue_detail_if_available(self, project: Project, analytics_api: AnalyticsApi):
        issues = analytics_api.get_issues(project.id)
        issue_id = extract_first_id(issues)
        if issue_id:
            detail = analytics_api.get_issue_detail(project.id, issue_id)
            assert isinstance(detail, dict)

    def test_query_settings(self, project: Project, analytics_api: AnalyticsApi):
        response = analytics_api.post_query_settings(project.id, settings={"query": "failures", "config": {}})
        assert isinstance(response, dict)
