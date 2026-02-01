import pytest


@pytest.mark.selenium
@pytest.mark.regression
def test_delete_creation_project(selenium_app, created_project_selenium):
    selenium_app.project_page.go_to_settings()

    selenium_app.project_page.delete_project()

    selenium_app.project_page.verify_project_deletion_started()
