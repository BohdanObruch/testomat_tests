from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.components.new_suite import NewSuite


class Suite(NewSuite):
    SUITE_NAME = (By.CSS_SELECTOR, ".edit-in-place")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_loaded(self):
        self.wait.for_visible(self.PANEL)
        self.wait.for_visible(self.HEADER)
        self.wait.for_visible(self.SAVE_BUTTON)
        self.wait.for_visible(self.CONTENT)
        self.wait.for_visible(self.TITLE_INPUT)
        return self

    def suite_name_is(self, expected_name: str):
        actual = self.get_text(self.SUITE_NAME).strip()
        assert actual == expected_name
        return self

    def tab_name_is_active(self, tab_name: str):
        tab = self.find((By.XPATH, f"//li[@role='tab' and .//text()[normalize-space()='{tab_name}']]"))
        class_name = tab.get_attribute("class") or ""
        assert "ember-tabs__tab--selected" in class_name
        return self
