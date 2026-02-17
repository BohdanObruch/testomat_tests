from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage


class AddTestMenu(BasePage):
    MENU = (By.CSS_SELECTOR, "ul[data-ember-action]")
    FOLDER_BUTTON = (By.XPATH, "//ul[@data-ember-action]//button[starts-with(normalize-space(),'Folder')]")
    SUITE_BUTTON = (By.XPATH, "//ul[@data-ember-action]//button[starts-with(normalize-space(),'Suite')]")
    REQUIREMENTS_BUTTON = (
        By.XPATH,
        "//ul[@data-ember-action]//button[starts-with(normalize-space(),'Tests From Requirement')]",
    )

    FOLDER_DESCRIPTION = (By.XPATH, "//ul[@data-ember-action]//p[contains(normalize-space(),'Collection of suites')]")
    SUITE_DESCRIPTION = (
        By.XPATH,
        "//ul[@data-ember-action]//p[contains(normalize-space(),'Collection of test cases')]",
    )
    REQUIREMENTS_DESCRIPTION = (
        By.XPATH,
        "//ul[@data-ember-action]//p[contains(normalize-space(),'Use AI to generate tests from the requirement')]",
    )

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Verify add test menu is loaded")
    def is_loaded(self):
        self.wait.for_visible(self.MENU)
        self.wait.for_visible(self.FOLDER_BUTTON)
        self.wait.for_visible(self.SUITE_BUTTON)
        self.wait.for_visible(self.REQUIREMENTS_BUTTON)
        return self

    @allure.step("Verify add test menu descriptions")
    def expect_descriptions(self):
        self.wait.for_visible(self.FOLDER_DESCRIPTION)
        self.wait.for_visible(self.SUITE_DESCRIPTION)
        self.wait.for_visible(self.REQUIREMENTS_DESCRIPTION)
        return self

    @allure.step("Click add folder")
    def click_folder(self):
        self.click(self.FOLDER_BUTTON)
        return self

    @allure.step("Click add suite")
    def click_suite(self):
        self.click(self.SUITE_BUTTON)
        return self

    @allure.step("Click tests from requirement")
    def click_tests_from_requirement(self):
        self.click(self.REQUIREMENTS_BUTTON)
        return self
