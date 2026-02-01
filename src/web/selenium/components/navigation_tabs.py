from __future__ import annotations

import re

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage


class NavigationTabs(BasePage):
    TABS_NAV = (By.XPATH, "//nav[@aria-label='Tabs']")
    SELECT_ALL_BUTTON = (By.CSS_SELECTOR, "//nav[aria-label='Tabs'] button [class*='checkbox-multiple-marked']")

    MANUAL_TAB = (By.XPATH, "//nav[@aria-label='Tabs']//a[.//text()[normalize-space()='Manual']]")
    AUTOMATED_TAB = (By.XPATH, "//nav[@aria-label='Tabs']//a[.//text()[normalize-space()='Automated']]")
    OUT_OF_SYNC_TAB = (By.XPATH, "//nav[@aria-label='Tabs']//a[.//text()[normalize-space()='Out of sync']]")
    DETACHED_TAB = (By.XPATH, "//nav[@aria-label='Tabs']//a[.//text()[normalize-space()='Detached']]")
    STARRED_TAB = (By.XPATH, "//nav[@aria-label='Tabs']//a[.//text()[normalize-space()='Starred']]")

    DISPLAY_BUTTON = (By.XPATH, "//button[normalize-space()='Display']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def is_loaded(self):
        self.wait.for_visible(self.TABS_NAV)
        self.wait.for_visible(self.MANUAL_TAB)
        self.wait.for_visible(self.AUTOMATED_TAB)
        return self

    def click_select_all(self):
        self.click(self.SELECT_ALL_BUTTON)
        return self

    def click_manual(self):
        self.click(self.MANUAL_TAB)
        return self

    def click_automated(self):
        self.click(self.AUTOMATED_TAB)
        return self

    def click_out_of_sync(self):
        self.click(self.OUT_OF_SYNC_TAB)
        return self

    def click_detached(self):
        self.click(self.DETACHED_TAB)
        return self

    def click_starred(self):
        self.click(self.STARRED_TAB)
        return self

    def open_display(self):
        self.click(self.DISPLAY_BUTTON)
        return self

    def link_by_name(self, name: str):
        return self.find((By.XPATH, f"//nav[@aria-label='Tabs']//a[.//text()[normalize-space()='{name}']]"))

    def counter_by_name(self, name: str):
        link = self.link_by_name(name)
        return link.find_element(By.CSS_SELECTOR, ".new-counter")

    def expect_tab_active(self, name: str):
        link = self.link_by_name(name)
        class_name = link.get_attribute("class") or ""
        assert re.search(r"\bactive\b", class_name)
        return self

    def expect_tab_count(self, name: str, expected_count: int):
        counter = self.counter_by_name(name)
        assert counter.text.strip() == str(expected_count)
        return self
