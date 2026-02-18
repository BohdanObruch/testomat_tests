import allure
import pytest

from src.api.controllers import PlanApi
from src.api.models import CaseModel, Project


@pytest.mark.api
@pytest.mark.regression
class TestPlans:
    def test_list_plans(self, project: Project, plan_api: PlanApi):
        with allure.step("List plans for project"):
            response = plan_api.list(project.id)
            assert isinstance(response.data, list)

    def test_plan_aux(self, project: Project, plan_api: PlanApi, created_test: CaseModel):
        with allure.step("Get plan counters"):
            assert isinstance(plan_api.count(project.id), dict)

        with allure.step("Validate plan query by test tag"):
            tag = None
            if created_test.attributes and created_test.attributes.tags:
                tag = created_test.attributes.tags[0]
            if not tag:
                tag = "plan_tag"
            payload = {"query": f"=tag == '{tag}'"}
            assert isinstance(plan_api.validate(project.id, payload=payload), dict)
