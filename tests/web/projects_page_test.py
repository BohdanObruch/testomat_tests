from src.web.application import Application
from src.web.components.project_card import Badges

TARGET_PROJECT = "python manufacture"


def test_search_project_in_company(login, app: Application):
    app.projects_page.navigate()

    app.projects_page.verify_page_loaded()

    app.projects_page.header.check_selected_company("QA Club Lviv")
    app.projects_page.header.plan_name_should_be("Enterprise plan")

    app.projects_page.header.search_project(TARGET_PROJECT)
    app.projects_page.count_of_project_visible(1)
    target_project = app.projects_page.get_project_by_title(TARGET_PROJECT)
    target_project.badges_has(Badges.Demo)


def test_should_be_possible_to_open_free_project(login, app: Application):
    app.projects_page.navigate()
    app.projects_page.header.select_company("Free Projects")
    app.projects_page.header.search_project(TARGET_PROJECT)

    app.projects_page.expect_project_heading_hidden(TARGET_PROJECT)
    app.projects_page.expect_no_projects_message()


def test_can_not_create_project_without_company(login, app: Application):
    app.projects_page.navigate()
    app.projects_page.header.select_company("Free Projects")
    app.projects_page.header.click_create()

    app.projects_page.expect_info_message("Please switch to a company you own to create a project")


def test_change_view_projects_list_by_table_view(login, app: Application):
    app.projects_page.navigate()
    app.projects_page.header.switch_to_table_view()

    app.projects_page.expect_table_view_active()
