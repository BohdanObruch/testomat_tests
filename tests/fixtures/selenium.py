import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.web.selenium.application import SeleniumApplication


def _is_headed_enabled(config: pytest.Config) -> bool:
    try:
        return bool(config.getoption("headed"))
    except Exception:
        return False


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest):
    options = Options()
    headless = not _is_headed_enabled(request.config)
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def selenium_app(driver, configs):
    app = SeleniumApplication(driver, configs.app_base_url)
    app.login(configs.email, configs.password)
    app.projects_page.navigate()
    return app


@pytest.fixture(scope="function")
def created_project_selenium(selenium_app):
    project_name = Faker().company()
    (
        selenium_app.new_projects_page.open()
        .is_loaded()
        .fill_project_title(project_name)
        .click_create()
        .is_loaded_empty_project()
        .empty_project_name_is(project_name)
        .close_read_me()
    )
    return project_name
