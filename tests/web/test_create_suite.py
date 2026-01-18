import pytest
from faker import Faker

from src.web.application import Application

TARGET_PROJECT = "Books"


@pytest.mark.regression
@pytest.mark.web
def test_create_test_suite(logged_app: Application):
    suite_title_name = Faker().company()
    suite_description = Faker().paragraph()

    logged_app.projects_page.navigate()
    logged_app.projects_page.header.search_project(TARGET_PROJECT)
    logged_app.projects_page.click_project_by_title(TARGET_PROJECT)

    (logged_app.project_page.is_loaded_project().project_name_is(TARGET_PROJECT)).open_add_test_dropdown()
    logged_app.project_page.test_menu.is_loaded().click_suite()

    (
        logged_app.project_page.add_suite.is_loaded()
        .fill_suite_title(suite_title_name)
        .fill_description(suite_description)
        .click_save()
    )

    (logged_app.project_page.suite.is_loaded().suite_name_is(suite_title_name).tab_name_is_active("Tests"))

    (logged_app.project_page.verify_suite_is_present(suite_title_name))
