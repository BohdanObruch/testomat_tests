import pytest

from src.web.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(logged_app: Application):
    logged_app.projects_page.header.plan_name_should_be("Enterprise plan")
    logged_app.projects_page.header.select_company("Free Projects")
    logged_app.projects_page.expect_no_projects_message()
    logged_app.projects_page.header.plan_name_should_be("free plan")
    logged_app.projects_page.header.free_plan_label.hover(force=True)
    logged_app.projects_page.expect_tooltip_message("You have a free subscription")
