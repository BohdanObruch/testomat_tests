import allure
import pytest
from faker import Faker

from src.api.controllers import TemplateApi
from src.api.models import Project, Template

fake = Faker()


@pytest.mark.api
@pytest.mark.regression
class TestTemplates:
    def test_list_templates(self, project: Project, template_api: TemplateApi):
        with allure.step("List templates for project"):
            response = template_api.list(project.id)
            assert isinstance(response.data, list)

    def test_create_get_update_delete_template(
        self,
        project: Project,
        template_api: TemplateApi,
        created_template: Template,
    ):
        with allure.step("Fetch created template by id"):
            fetched = template_api.get_by_id(project.id, created_template.id).data
            assert fetched.id == created_template.id

        with allure.step("Update template"):
            title = (
                f"{created_template.attributes.title} updated"
                if created_template.attributes and created_template.attributes.title
                else fake.sentence()
            )
            update_payload = {
                "data": {
                    "type": "templates",
                    "attributes": {
                        "title": title,
                        "kind": "test",
                        "body": "### Updated",
                    },
                }
            }
            updated = template_api.update(project.id, created_template.id, update_payload).data
            assert updated.id == created_template.id

    def test_template_defaults_and_refresh(self, project: Project, template_api: TemplateApi):
        with allure.step("Get default template by kind"):
            assert isinstance(template_api.get_default_for_kind(project.id, "test"), dict)
        with allure.step("Refresh templates cache"):
            assert isinstance(template_api.refresh(project.id), dict)
