import pytest
from faker import Faker

from src.api.controllers import TemplateApi
from src.api.models import Project, Template

fake = Faker()


@pytest.mark.api
class TestTemplates:
    def test_list_templates(self, project: Project, template_api: TemplateApi):
        response = template_api.list(project.id)
        assert isinstance(response.data, list)

    def test_create_get_update_delete_template(
        self,
        project: Project,
        template_api: TemplateApi,
        created_template: Template,
    ):
        fetched = template_api.get_by_id(project.id, created_template.id).data
        assert fetched.id == created_template.id

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
        assert isinstance(template_api.get_default_for_kind(project.id, "test"), dict)
        assert isinstance(template_api.refresh(project.id), dict)
