from __future__ import annotations

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage


class NewSuite(BasePage):
    PANEL = (By.CSS_SELECTOR, ".detail")
    HEADER = (By.CSS_SELECTOR, ".detail-view-header")
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")
    CANCEL_LINK = (By.XPATH, "//a[normalize-space()='Cancel']")
    HEADER_CLOSE_BUTTON = (By.CSS_SELECTOR, ".detail-view-actions .third-btn")

    CONTENT = (By.CSS_SELECTOR, ".detail-view-content")
    TITLE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Title']")
    DESCRIPTION_IFRAME = (By.CSS_SELECTOR, ".editor-suite iframe")
    DESCRIPTION_SURFACE = (By.CSS_SELECTOR, ".monaco-editor .view-lines")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea.inputarea")

    SELECT_SUITE_HEADING = (By.XPATH, "//*[normalize-space()='Select suite for test']")
    SUITE_CHECKBOXES = (By.CSS_SELECTOR, ".tree-branch")  # .tree-branch input
    SELECT_BUTTON = (By.XPATH, "//button[normalize-space()='Select']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Verify new suite selector is loaded")
    def is_loaded(self):
        self.wait.for_visible(self.SELECT_SUITE_HEADING)
        self.wait.for_visible(self.SUITE_CHECKBOXES)
        return self

    @allure.step("Select first suite")
    def select_first_suite(self):
        checkboxes = self.find_all(self.SUITE_CHECKBOXES)
        checkboxes[0].click()
        self.click(self.SELECT_BUTTON)
        return self

    @allure.step("Set suite title: {title}")
    def set_suite_title(self, title: str):
        self.type_text(self.TITLE_INPUT, title)
        return self

    @allure.step("Save suite")
    def click_save(self):
        self.click(self.SAVE_BUTTON)
        return self

    @allure.step("Cancel suite editing")
    def click_cancel(self):
        self.click(self.CANCEL_LINK)
        return self

    @allure.step("Close suite panel with header button")
    def close_with_header_button(self):
        self.click(self.HEADER_CLOSE_BUTTON)
        return self

    @allure.step("Fill suite title: {title}")
    def fill_suite_title(self, title: str):
        self.type_text(self.TITLE_INPUT, title)
        return self

    @allure.step("Fill suite description")
    def fill_description(self, text: str):
        self.wait.for_frame(self.DESCRIPTION_IFRAME)
        self.click(self.DESCRIPTION_SURFACE)
        editor = self.wait.for_present(self.DESCRIPTION_INPUT)
        self.driver.execute_script("arguments[0].focus();", editor)
        editor.send_keys(text)
        self.driver.switch_to.default_content()
        return self
