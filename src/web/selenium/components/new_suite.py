from __future__ import annotations

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
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea.inputarea")

    SELECT_SUITE_HEADING = (By.XPATH, "//*[normalize-space()='Select suite for test']")
    SUITE_CHECKBOXES = (By.CSS_SELECTOR, ".tree-branch input")
    SELECT_BUTTON = (By.XPATH, "//button[normalize-space()='Select']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_loaded(self):
        self.wait.for_visible(self.SELECT_SUITE_HEADING)
        self.wait.for_visible(self.SUITE_CHECKBOXES)
        return self

    def select_first_suite(self):
        checkboxes = self.find_all(self.SUITE_CHECKBOXES)
        checkboxes[0].click()
        self.click(self.SELECT_BUTTON)
        return self

    def set_suite_title(self, title: str):
        self.type_text(self.TITLE_INPUT, title)
        return self

    def click_save(self):
        self.click(self.SAVE_BUTTON)
        return self

    def click_cancel(self):
        self.click(self.CANCEL_LINK)
        return self

    def close_with_header_button(self):
        self.click(self.HEADER_CLOSE_BUTTON)
        return self

    def fill_suite_title(self, title: str):
        self.type_text(self.TITLE_INPUT, title)
        return self

    def fill_description(self, text: str):
        self.wait.for_frame(self.DESCRIPTION_IFRAME)
        self.type_text(self.DESCRIPTION_INPUT, text)
        self.driver.switch_to.default_content()
        return self
