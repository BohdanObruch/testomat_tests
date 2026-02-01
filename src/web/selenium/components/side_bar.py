from __future__ import annotations

import re

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage


class SideBar(BasePage):
    MENU = (By.CSS_SELECTOR, ".mainnav-menu")
    LOGO = (By.CSS_SELECTOR, "button.btn-open")
    CLOSE_BUTTON = (By.XPATH, "//button[normalize-space()='Close']")

    TESTS_LINK = (By.XPATH, "//a[normalize-space()='Tests']")
    RUNS_LINK = (By.XPATH, "//a[normalize-space()='Runs']")
    PLANS_LINK = (By.XPATH, "//a[normalize-space()='Plans']")
    STEPS_LINK = (By.XPATH, "//a[normalize-space()='Steps']")
    PULSE_LINK = (By.XPATH, "//a[normalize-space()='Pulse']")
    IMPORTS_LINK = (By.XPATH, "//a[normalize-space()='Imports']")
    ANALYTICS_LINK = (By.XPATH, "//a[normalize-space()='Analytics']")
    BRANCHES_LINK = (By.XPATH, "//a[normalize-space()='Branches']")
    SETTINGS_LINK = (By.XPATH, "//a[normalize-space()='Settings']")

    HELP_LINK = (By.XPATH, "//a[normalize-space()='Help']")
    PROJECTS_LINK = (By.XPATH, "//a[normalize-space()='Projects']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_loaded(self):
        element = self.find_visible(self.MENU)
        ActionChains(self.driver).move_to_element(element).perform()
        self.find_visible(self.LOGO)
        return self

    def _click_link(self, locator):
        self.click(locator)
        return self

    def go_to_tests(self):
        return self._click_link(self.TESTS_LINK)

    def go_to_runs(self):
        return self._click_link(self.RUNS_LINK)

    def go_to_plans(self):
        return self._click_link(self.PLANS_LINK)

    def go_to_steps(self):
        return self._click_link(self.STEPS_LINK)

    def go_to_pulse(self):
        return self._click_link(self.PULSE_LINK)

    def go_to_imports(self):
        return self._click_link(self.IMPORTS_LINK)

    def go_to_analytics(self):
        return self._click_link(self.ANALYTICS_LINK)

    def go_to_branches(self):
        return self._click_link(self.BRANCHES_LINK)

    def go_to_settings(self):
        return self._click_link(self.SETTINGS_LINK)

    def go_to_help(self):
        return self._click_link(self.HELP_LINK)

    def go_to_projects(self):
        return self._click_link(self.PROJECTS_LINK)

    def click_logo(self):
        self.click(self.LOGO)
        return self

    def close_menu(self):
        self.click(self.CLOSE_BUTTON)
        return self

    def link_by_name(self, name: str):
        return self.find((By.XPATH, f"//a[normalize-space()='{name}']"))

    def expect_tab_active(self, name: str):
        link = self.link_by_name(name)
        class_name = link.get_attribute("class") or ""
        assert re.search(r"\bactive\b", class_name)
        return self
