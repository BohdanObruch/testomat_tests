from faker import Faker

from src.web.application import Application

TARGET_PROJECT = "python manufacture"


def test_create_test_suite(login, app: Application):
    suite_title_name = Faker().company()
    suite_description = Faker().paragraph()

    app.projects_page.navigate()
    app.projects_page.header.search_project(TARGET_PROJECT)
    app.projects_page.click_project_by_title(TARGET_PROJECT)

    (app.project_page
     .is_loaded_project()
     .project_name_is(TARGET_PROJECT)).open_add_test_dropdown()
    app.project_page.test_menu.is_loaded().click_suite()

    (app.project_page
     .add_suite
     .is_loaded()
     .fill_suite_title(suite_title_name)
     .fill_description(suite_description)
     .click_save())

    (app.project_page
     .suite
     .is_loaded()
     .suite_name_is(suite_title_name)
     .tab_name_is_active("Tests"))

    (app.project_page
     .verify_suite_is_present(suite_title_name))
