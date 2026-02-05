import pytest


@pytest.mark.selenium
@pytest.mark.smoke
def test_projects_page_header(selenium_app):
    selenium_app.projects_page.header.plan_name_should_be("Enterprise Plan")
    selenium_app.projects_page.header.select_company("Free Projects")
    selenium_app.projects_page.expect_no_projects_message()
    selenium_app.projects_page.header.plan_name_should_be("Free Plan")
    selenium_app.projects_page.header.hover_free_plan_label()
    selenium_app.projects_page.expect_tooltip_message("You have a free subscription")
