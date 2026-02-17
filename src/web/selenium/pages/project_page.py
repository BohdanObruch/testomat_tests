from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.web.selenium.components import AddTestMenu, NavigationTabs, NewSuite, SideBar, Suite, TestModal
from src.web.selenium.core.base_page import BasePage


class ProjectPage(BasePage):
    HEADER = (By.CSS_SELECTOR, ".sticky-header")
    NAVIGATION_MENU = (By.CSS_SELECTOR, ".mainnav-menu")
    PLACEHOLDER = (By.CSS_SELECTOR, "[placeholder='First Suite']")
    CREATE_SUITE_BUTTON = (By.XPATH, "//button[normalize-space()='Suite']")
    ADD_TEST_BUTTON = (By.XPATH, "//button[starts-with(normalize-space(.), 'Test')]")
    ADD_TEST_DROPDOWN = (
        By.XPATH,
        "//button[starts-with(normalize-space(.), 'Test')]/following-sibling::div[contains(@class,'ember-basic-dropdown')]",
    )
    EMPTY_PROJECT_NAME = (By.CSS_SELECTOR, ".sticky-header h2")
    BREADCRUMBS_PAGE = (By.CSS_SELECTOR, ".breadcrumbs-page")
    PROJECT_NAME = (By.CSS_SELECTOR, ".breadcrumbs-page a")
    README_CLOSE_BUTTON = (By.CSS_SELECTOR, ".back .third-btn")
    SUITES = (By.CSS_SELECTOR, ".dragSortList")
    SUITE_ITEM = (By.CSS_SELECTOR, ".dragSortItem")
    SUITE_NAME = (By.CSS_SELECTOR, ".dragSortItem .ember-view span")
    SETTINGS_LINK = (By.XPATH, "//a[contains(normalize-space(),'Settings')]")
    PROJECT_MENU_SETTINGS = (By.CSS_SELECTOR, ".subnav-menu-settings")
    ADMINISTRATION_BUTTON = (By.XPATH, "//button[normalize-space()='Administration']")
    DELETE_PROJECT_TEXT = (By.XPATH, "//*[normalize-space()='Delete Project']")
    DELETE_PROJECT_BUTTON = (By.XPATH, "//button[normalize-space()='Delete Project']")
    DELETION_WARNING = (
        By.XPATH,
        "//*[contains(normalize-space(),'Project will be deleted in few minutes')]",
    )

    def __init__(self, driver: WebDriver, base_url: str = ""):
        super().__init__(driver)
        self.base_url = base_url.rstrip("/")
        self.side_bar = SideBar(driver)
        self.navigation_tabs = NavigationTabs(driver)
        self.test_menu = AddTestMenu(driver)
        self.add_suite = Suite(driver)
        self.test_modal = TestModal(driver)
        self.suite = Suite(driver)
        self.new_suite = NewSuite(driver)

    def _url(self, path: str) -> str:
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"

    @allure.step("Open project with id: {project_id}")
    def open_by_id(self, project_id: str):
        self.driver.get(self._url(f"/projects/{project_id}"))
        return self

    @allure.step("Verify empty project is loaded")
    def is_loaded_empty_project(self):
        self.wait.for_visible(self.HEADER)
        self.wait.for_visible(self.NAVIGATION_MENU)
        self.wait.for_visible(self.PLACEHOLDER)
        self.wait.for_visible(self.CREATE_SUITE_BUTTON)
        return self

    @allure.step("Verify project is loaded")
    def is_loaded_project(self):
        self.wait.for_visible(self.HEADER)
        self.wait.for_visible(self.NAVIGATION_MENU)
        self.wait.for_visible(self.ADD_TEST_BUTTON)
        return self

    @allure.step("Verify project name is: {expected_project_name}")
    def empty_project_name_is(self, expected_project_name: str):
        assert self.get_text(self.EMPTY_PROJECT_NAME).strip() == expected_project_name
        return self

    @allure.step("Verify breadcrumb project name is: {expected_project_name}")
    def project_name_is(self, expected_project_name: str):
        assert self.get_text(self.PROJECT_NAME).strip() == expected_project_name.capitalize()
        return self

    @allure.step("Close read me panel")
    def close_read_me(self):
        self.click(self.README_CLOSE_BUTTON)
        return self

    @allure.step("Click add test button")
    def click_add_test(self):
        self.click(self.ADD_TEST_BUTTON)
        return self

    @allure.step("Open add test dropdown")
    def open_add_test_dropdown(self):
        self.click(self.ADD_TEST_DROPDOWN)
        return self

    @allure.step("Verify suite is present: {suite_name}")
    def verify_suite_is_present(self, suite_name: str):
        suites = [element.text.strip() for element in self.find_all(self.SUITE_NAME)]
        assert suite_name in suites, f"Suite '{suite_name}' not found in project."
        return self

    @allure.step("Open project settings")
    def go_to_settings(self):
        self.click(self.SETTINGS_LINK)
        self.wait.for_visible(self.PROJECT_MENU_SETTINGS)
        return self

    def _accept_alert_if_present(self, timeout: int = 3):
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert.accept()
        except Exception:
            return False
        return True

    @allure.step("Delete project")
    def delete_project(self):
        self.click(self.ADMINISTRATION_BUTTON)
        self._accept_alert_if_present()
        self.click(self.DELETE_PROJECT_BUTTON)
        self._accept_alert_if_present()
        return self

    @allure.step("Verify project deletion started")
    def verify_project_deletion_started(self):
        self.wait.for_visible(self.DELETION_WARNING)
        return self

    @allure.step("Create test suite via popup")
    def create_test_suite_via_popup(self):
        self.click((By.CSS_SELECTOR, ".md-icon-chevron-down"))
        self.click((By.XPATH, "//*[normalize-space()='Collection of test cases']"))
        return self

    @allure.step("Verify suite with name is visible: {test_suite_name}")
    def suite_with_name_is_visible(self, test_suite_name: str):
        self.wait.for_visible(
            (By.XPATH, f"//*[contains(@class,'suites-list-content')]//*[normalize-space()='{test_suite_name}']")
        )
        return self

    @allure.step("Create test via popup")
    def create_test_via_popup(self):
        self.click(self.ADD_TEST_BUTTON)
        return self

    @allure.step("Create first suite: {target_suite_name}")
    def create_first_suite(self, target_suite_name: str):
        self.type_text(self.PLACEHOLDER, target_suite_name)
        self.click(self.CREATE_SUITE_BUTTON)
        self.wait.for_invisible(self.CREATE_SUITE_BUTTON)
        return self
