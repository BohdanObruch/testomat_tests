from __future__ import annotations

from src.api.controllers.base_controller import BaseController


class AnalyticsApi(BaseController):
    def get_jira_stats(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/jira", params={"envs": envs, "tags": tags})

    def get_jira_issue(self, project_id: str, issue_id: str) -> dict:
        return self._get(f"/api/{project_id}/analytics/jira/{issue_id}")

    def get_labels_stats(
        self,
        project_id: str,
        envs: str | None = None,
        tags: str | None = None,
        labels: str | None = None,
    ) -> dict:
        return self._get(
            f"/api/{project_id}/analytics/labels",
            params={"envs": envs, "tags": tags, "labels": labels},
        )

    def get_label_detail(self, project_id: str, label_id: str, strategy: str | None = None) -> dict:
        return self._get(
            f"/api/{project_id}/analytics/labels/{label_id}",
            params={"strategy": strategy},
        )

    def get_runenvs_stats(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(
            f"/api/{project_id}/analytics/runenvs",
            params={"envs": envs, "tags": tags},
        )

    def get_runenv_detail(self, project_id: str, env_id: str) -> dict:
        return self._get(f"/api/{project_id}/analytics/runenvs/{env_id}")

    def get_tags_stats(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/tags", params={"envs": envs, "tags": tags})

    def get_tag_detail(self, project_id: str, tag_id: str) -> dict:
        return self._get(f"/api/{project_id}/analytics/tags/{tag_id}")

    def get_automation(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/automation", params={"envs": envs, "tags": tags})

    def get_counters(
        self,
        project_id: str,
        envs: str | None = None,
        tags: str | None = None,
        chosen_items: str | None = None,
        reload: bool | None = None,
    ) -> dict:
        return self._get(
            f"/api/{project_id}/analytics/counters",
            params={"envs": envs, "tags": tags, "chosen_items": chosen_items, "reload": reload},
        )

    def get_defect_detail(self, project_id: str, defect_id: str) -> dict:
        return self._get(f"/api/{project_id}/analytics/defects/{defect_id}")

    def get_failing(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/failing", params={"envs": envs, "tags": tags})

    def get_failures(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/failures", params={"envs": envs, "tags": tags})

    def get_flaky(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/flaky", params={"envs": envs, "tags": tags})

    def get_issues(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/issues", params={"envs": envs, "tags": tags})

    def get_issue_detail(self, project_id: str, issue_id: str) -> dict:
        return self._get(f"/api/{project_id}/analytics/issues/{issue_id}")

    def get_pending(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/pending", params={"envs": envs, "tags": tags})

    def get_slow(self, project_id: str, envs: str | None = None, tags: str | None = None) -> dict:
        return self._get(f"/api/{project_id}/analytics/slow", params={"envs": envs, "tags": tags})

    def post_query_settings(self, project_id: str, settings: dict) -> dict:
        return self._post(f"/api/{project_id}/analytics/query_settings", data=settings)
