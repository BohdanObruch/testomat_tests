import pytest
from faker import Faker

from api import ApiClient
from src.web.application import Application


@pytest.mark.regression
@pytest.mark.web
def test_new_project_creation(logged_app: Application, created_project):
    logged_app.project_page.side_bar.is_loaded().click_logo().expect_tab_active("Tests")


@pytest.mark.smoke
@pytest.mark.web
def test_new_project_creation_and_test_popup(logged_app: Application):
    target_project_name = Faker().company()

    (logged_app.new_projects_page.open().is_loaded().fill_project_title(target_project_name).click_create())

    project_page = logged_app.project_page
    (project_page.is_loaded_empty_project().empty_project_name_is(target_project_name).close_read_me())

    (project_page.side_bar.is_loaded().click_logo().expect_tab_active("Tests"))

    target_suite_name = Faker().company()
    project_page.create_first_suite(target_suite_name)
    project_page.create_test_via_popup()
    project_page.new_suite.is_loaded().select_first_suite()

    test_name = Faker().sentence()
    project_page.test_modal.is_loaded("test").set_title(test_name).save()
    project_page.test_modal.edit_is_visible("test")


@pytest.mark.smoke
@pytest.mark.web
def test_open_project_and_create_test_suite_from_side_bar(api_client: ApiClient, logged_app: Application):
    all_projects = api_client.get_projects()
    target_project_id = all_projects[0].id

    logged_app.project_page.open_by_id(target_project_id).side_bar.is_loaded()
    logged_app.project_page.create_test_suite_via_popup()

    test_name = Faker().sentence()
    logged_app.project_page.test_modal.is_loaded("Suite").set_title(test_name).save()
    logged_app.project_page.suite_with_name_is_visible(test_name)


@pytest.mark.smoke
@pytest.mark.web
def test_choose_project_by_classic_mode(logged_app: Application):
    logged_app.projects_page.header.click_create()

    logged_app.new_projects_page.is_loaded()

    logged_app.new_projects_page.expect_mode_selected("classical")


@pytest.mark.smoke
@pytest.mark.web
def test_choose_project_by_bdd_mode(logged_app: Application):
    logged_app.projects_page.header.click_create()
    logged_app.new_projects_page.is_loaded()

    logged_app.new_projects_page.select_mode("bdd")
    logged_app.new_projects_page.expect_mode_selected("bdd")


@pytest.mark.smoke
@pytest.mark.web
def test_can_create_project_by_header_button(logged_app: Application):
    logged_app.projects_page.open_new_project_from_header()

    logged_app.new_projects_page.is_loaded()
