import pytest
from faker import Faker

from src.api.controllers import RunApi, RunGroupApi
from src.api.models import Project, Run, RunGroup

fake = Faker()


@pytest.mark.api
class TestRunGroups:
    def test_list_rungroups(self, project: Project, rungroup_api: RunGroupApi):
        response = rungroup_api.list(project.id)
        assert isinstance(response.data, list)

    def test_create_update_delete_rungroup(
        self,
        project: Project,
        rungroup_api: RunGroupApi,
        created_rungroup: RunGroup,
    ):
        fetched = rungroup_api.get_by_id(project.id, created_rungroup.id).data
        assert fetched.id == created_rungroup.id

        update_payload = {"data": {"type": "rungroups", "attributes": {"title": fake.sentence()}}}
        updated = rungroup_api.update(project.id, created_rungroup.id, update_payload).data
        assert updated.id == created_rungroup.id

    def test_rungroup_aux(self, project: Project, rungroup_api: RunGroupApi, created_rungroup: RunGroup):
        assert isinstance(rungroup_api.archive(project.id, {"rungroups_ids": [created_rungroup.id]}), dict)
        assert isinstance(rungroup_api.unarchive(project.id, {"rungroups_ids": [created_rungroup.id]}), dict)
        assert isinstance(rungroup_api.copy(project.id, created_rungroup.id), dict)


@pytest.mark.api
class TestRuns:
    def test_list_runs(self, project: Project, run_api: RunApi):
        response = run_api.list(project.id)
        assert isinstance(response.data, list)

    def test_create_update_delete_run(self, project: Project, run_api: RunApi, created_run: Run):
        fetched = run_api.get_by_id(project.id, created_run.id).data
        assert fetched.id == created_run.id

        update_payload = {"data": {"type": "runs", "attributes": {"title": fake.sentence()}}}
        updated = run_api.update(project.id, created_run.id, update_payload).data
        assert updated.id == created_run.id
