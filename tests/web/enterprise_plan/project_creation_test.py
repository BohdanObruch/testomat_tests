import pytest

from src.web.application import Application


@pytest.mark.regression
@pytest.mark.web
def test_new_project_creation(logged_app: Application, created_project):
    logged_app.project_page.side_bar.is_loaded().click_logo().expect_tab_active("Tests")


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
