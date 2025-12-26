from faker import Faker

from src.web.application import Application


def test_new_project_creation(login, app: Application):
    target_project_name = Faker().company()

    (app.new_projects_page
     .open()
     .is_loaded()
     .fill_project_title(target_project_name)
     .click_create())

    (app.project_page
     .is_loaded()
     .empty_project_name_is(target_project_name)
     .close_read_me())

    (app.project_page
     .side_bar
     .is_loaded()
     .click_logo()
     .expect_tab_active("Tests"))


def test_choose_project_by_classic_mode(login, app: Application):
    app.projects_page.header.click_create()

    app.new_projects_page.is_loaded()

    app.new_projects_page.expect_mode_selected("classical")


def test_choose_project_by_bdd_mode(login, app: Application):
    app.projects_page.header.click_create()
    app.new_projects_page.is_loaded()

    app.new_projects_page.select_mode("bdd")
    app.new_projects_page.expect_mode_selected("bdd")


def test_can_create_project_by_header_button(login, app: Application):
    app.projects_page.open_new_project_from_header()

    app.new_projects_page.is_loaded()
