import pytest

from src.web.selenium.components import Badges

TARGET_PROJECT = "Books"


@pytest.mark.selenium
@pytest.mark.smoke
def test_search_project_in_company(selenium_app):
    selenium_app.projects_page.verify_page_loaded()

    selenium_app.projects_page.header.check_selected_company("QA Club Lviv")
    selenium_app.projects_page.header.plan_name_should_be("Enterprise Plan")

    selenium_app.projects_page.header.search_project(TARGET_PROJECT)
    selenium_app.projects_page.count_of_project_visible(1)
    target_project = selenium_app.projects_page.get_project_by_title(TARGET_PROJECT)
    target_project.badges_has(Badges.Classical)


@pytest.mark.selenium
@pytest.mark.smoke
def test_should_be_possible_to_open_free_project(selenium_app):
    selenium_app.projects_page.header.select_company("Free Projects")
    selenium_app.projects_page.header.search_project(TARGET_PROJECT)

    selenium_app.projects_page.expect_project_heading_hidden(TARGET_PROJECT)
    selenium_app.projects_page.expect_no_projects_message()


@pytest.mark.selenium
@pytest.mark.smoke
def test_can_not_create_project_without_company(selenium_app):
    selenium_app.projects_page.header.select_company("Free Projects")
    selenium_app.projects_page.header.click_create()

    selenium_app.projects_page.expect_info_message("Please switch to a company you own to create a project")


@pytest.mark.selenium
@pytest.mark.smoke
def test_change_view_projects_list_by_table_view(selenium_app):
    selenium_app.projects_page.header.switch_to_table_view()

    selenium_app.projects_page.expect_table_view_active()
