from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.components import ProjectCard, ProjectsHeader
from src.web.selenium.core.base_page import BasePage


class ProjectsPage(BasePage):
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".common-flash-success-right p")
    INFO_MESSAGE = (By.CSS_SELECTOR, ".common-flash-info-right p")
    PROJECTS_GRID = (By.CSS_SELECTOR, "#grid")
    PROJECT_CARDS = (By.CSS_SELECTOR, "#grid ul li a[href*='/projects/']")
    TABLE = (By.CSS_SELECTOR, "#table")
    EMPTY_PROJECTS_MESSAGE = (By.XPATH, "//*[contains(normalize-space(),'You have not created any projects yet')]")
    NEW_PROJECT_LINK = (By.CSS_SELECTOR, ".auth-header-nav [href='/projects/new']")
    TOTAL_COUNT = (By.CSS_SELECTOR, ".common-counter")

    def __init__(self, driver: WebDriver, base_url: str = ""):
        super().__init__(driver)
        self.base_url = base_url.rstrip("/")
        self.header = ProjectsHeader(driver)

    def _url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"

    @allure.step("Navigate to projects page: {url}")
    def navigate(self, url: str = "/projects"):
        self.driver.get(self._url(url))
        return self

    @allure.step("Get success message text")
    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_MESSAGE).strip()

    @allure.step("Get all project cards")
    def get_projects(self) -> list[ProjectCard]:
        return [ProjectCard(card) for card in self.find_all(self.PROJECT_CARDS)]

    @allure.step("Get project card by title: {title}")
    def get_project_by_title(self, title: str) -> ProjectCard:
        for card in self.find_all(self.PROJECT_CARDS):
            heading = card.find_element(By.CSS_SELECTOR, "h3.text-gray-700")
            if heading.text.strip() == title:
                return ProjectCard(card)
        raise AssertionError(f"Project with title '{title}' not found.")

    @allure.step("Open project by title: {title}")
    def click_project_by_title(self, title: str):
        self.get_project_by_title(title).click()
        return self

    @allure.step("Verify visible project count is: {expected_count}")
    def count_of_project_visible(self, expected_count: int):
        visible_cards = [card for card in self.find_all(self.PROJECT_CARDS) if card.is_displayed()]
        assert len(visible_cards) == expected_count, f"Expected {expected_count} projects, got {len(visible_cards)}."
        return self

    @allure.step("Get total projects count")
    def get_total_projects(self) -> int:
        return int(self.get_text(self.TOTAL_COUNT))

    @allure.step("Search projects with query: {query}")
    def search_and_get_results(self, query: str) -> list[ProjectCard]:
        self.header.search_project(query)
        return self.get_projects()

    @allure.step("Verify projects page is loaded")
    def verify_page_loaded(self):
        self.wait.for_visible(self.header.PAGE_TITLE)
        self.wait.for_visible(self.PROJECTS_GRID)
        return self

    @allure.step("Verify success message is: {expected_text}")
    def verify_success_message(self, expected_text: str):
        assert self.get_text(self.SUCCESS_MESSAGE).strip() == expected_text
        return self

    @allure.step("Verify project heading is hidden: {title}")
    def expect_project_heading_hidden(self, title: str):
        locator = (By.XPATH, f"//h1[normalize-space()='{title}']|//h2[normalize-space()='{title}']")
        if self.is_displayed(locator):
            raise AssertionError(f"Project heading '{title}' should be hidden.")
        return self

    @allure.step("Verify no projects message is visible")
    def expect_no_projects_message(self):
        self.wait.for_visible(self.EMPTY_PROJECTS_MESSAGE)
        return self

    @allure.step("Verify info message is: {expected_text}")
    def expect_info_message(self, expected_text: str):
        assert self.get_text(self.INFO_MESSAGE).strip() == expected_text
        return self

    @allure.step("Verify tooltip message is: {expected_text}")
    def expect_tooltip_message(self, expected_text: str):
        tooltip = (By.XPATH, f"//*[normalize-space()='{expected_text}']")
        self.wait.for_visible(tooltip)
        return self

    @allure.step("Verify table view is active")
    def expect_table_view_active(self):
        self.wait.for_visible(self.TABLE)
        class_name = self.find(self.header.TABLE_VIEW_BUTTON).get_attribute("class") or ""
        assert "active_list_type" in class_name
        return self

    @allure.step("Open new project page from header")
    def open_new_project_from_header(self):
        self.click(self.NEW_PROJECT_LINK)
        return self

    @allure.step("Verify projects page login success flash is visible")
    def is_loaded(self):
        self.wait.for_visible((By.CSS_SELECTOR, ".common-flash-success"))
        return self
