import contextlib

import allure
import pytest
from faker import Faker
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from src.web.selenium.application import SeleniumApplication
from tests.fixtures.settings import PlaywrightSettings


def _is_headed_enabled(config: pytest.Config) -> bool:
    with contextlib.suppress(ValueError, TypeError, AttributeError):
        return bool(config.getoption("headed"))
    return False


def _test_failed(request: pytest.FixtureRequest) -> bool:
    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    return bool((rep_setup and rep_setup.failed) or (rep_call and rep_call.failed))


def _normalized_option(value: str | None) -> str:
    return (value or "off").lower()


def _should_take_screenshot(settings: PlaywrightSettings, request: pytest.FixtureRequest) -> bool:
    mode = _normalized_option(settings.screenshot)
    if mode == "on":
        return True
    if mode == "only-on-failure":
        return _test_failed(request)
    return False


def _artifact_basename(request: pytest.FixtureRequest) -> str:
    name = request.node.nodeid
    return name.replace("::", "__").replace("/", "_").replace("\\", "_").replace("[", "_").replace("]", "_")


def _capture_screenshot(driver: WebDriver, request: pytest.FixtureRequest, settings: PlaywrightSettings) -> None:
    if not _should_take_screenshot(settings, request):
        return

    screenshot_bytes: bytes | None = None
    with contextlib.suppress(WebDriverException):
        screenshot_bytes = driver.get_screenshot_as_png()

    if not screenshot_bytes:
        return

    artifact_name = _artifact_basename(request)
    allure.attach(screenshot_bytes, name=artifact_name, attachment_type=allure.attachment_type.PNG)

    settings.screenshot_dir.mkdir(parents=True, exist_ok=True)
    with contextlib.suppress(OSError):
        (settings.screenshot_dir / f"{artifact_name}.png").write_bytes(screenshot_bytes)


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest, playwright_settings: PlaywrightSettings):
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

    _capture_screenshot(driver, request, playwright_settings)
    with contextlib.suppress(WebDriverException):
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
