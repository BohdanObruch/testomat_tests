from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage
from src.web.selenium.pages.project_page import ProjectPage


class NewProjectsPage(BasePage):
    FORM_CONTAINER = (By.CSS_SELECTOR, "#content-desktop [action='/projects']")
    CLASSICAL_MODE = (By.CSS_SELECTOR, "#classical")
    BDD_MODE = (By.CSS_SELECTOR, "#bdd")
    PROJECT_TITLE = (By.CSS_SELECTOR, "#project_title")
    DEMO_BUTTON = (By.CSS_SELECTOR, "#demo-btn")
    CREATE_BUTTON = (By.CSS_SELECTOR, "#project-create-btn input")

    def __init__(self, driver: WebDriver, base_url: str = ""):
        super().__init__(driver)
        self.base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"

    def open(self):
        self.driver.get(self._url("/projects/new"))
        return self

    def is_loaded(self):
        self.wait.for_visible(self.FORM_CONTAINER)
        self.wait.for_visible(self.CLASSICAL_MODE)
        self.wait.for_visible(self.BDD_MODE)
        self.wait.for_visible(self.PROJECT_TITLE)
        self.wait.for_visible(self.DEMO_BUTTON)
        self.wait.for_visible(self.CREATE_BUTTON)
        return self

    def fill_project_title(self, target_project_name: str):
        self.type_text(self.PROJECT_TITLE, target_project_name)
        return self

    def click_create(self) -> ProjectPage:
        self.click(self.CREATE_BUTTON)
        self.wait.for_invisible(self.CREATE_BUTTON)
        return ProjectPage(self.driver, self.base_url)

    def select_mode(self, mode: str):
        self.click((By.CSS_SELECTOR, f"#{mode}"))
        return self

    def expect_mode_selected(self, mode: str):
        button = self.find((By.CSS_SELECTOR, f"#{mode}"))
        icon = self.find((By.CSS_SELECTOR, f"#{mode}-img"))
        assert button.value_of_css_property("border-color") == "rgb(79, 70, 229)"
        assert icon.get_attribute("src").endswith("/images/projects/circle-tick-dark-mode.svg")
        return self
