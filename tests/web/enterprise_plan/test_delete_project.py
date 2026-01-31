import pytest

from src.web.application import Application


@pytest.mark.regression
@pytest.mark.web
def test_delete_creation_project(logged_app: Application, created_project):
    logged_app.project_page.go_to_settings()

    logged_app.project_page.delete_project()

    logged_app.project_page.verify_project_deletion_started()
