from __future__ import annotations

import re

import allure
from playwright.sync_api import Page, expect


class NavigationTabs:
    def __init__(self, page: Page):
        self.page = page

        self._tabs_nav = page.get_by_role("navigation", name="Tabs")
        self._select_all_button = self._tabs_nav.locator("button [class*=checkbox-multiple-marked]")

        self._manual_tab = self._tabs_nav.get_by_role("link", name="Manual")
        self._automated_tab = self._tabs_nav.get_by_role("link", name="Automated")
        self._out_of_sync_tab = self._tabs_nav.get_by_role("link", name="Out of sync")
        self._detached_tab = self._tabs_nav.get_by_role("link", name="Detached")
        self._starred_tab = self._tabs_nav.get_by_role("link", name="Starred")

        self._display_button = page.get_by_role("button", name="Display")

    @allure.step("Verify navigation tabs are loaded")
    def is_loaded(self) -> NavigationTabs:
        expect(self._tabs_nav).to_be_visible()
        expect(self._manual_tab).to_be_visible()
        expect(self._automated_tab).to_be_visible()
        return self

    @allure.step("Click select all tab items")
    def click_select_all(self) -> NavigationTabs:
        self._select_all_button.click()
        return self

    @allure.step("Open Manual tab")
    def click_manual(self) -> NavigationTabs:
        self._manual_tab.click()
        return self

    @allure.step("Open Automated tab")
    def click_automated(self) -> NavigationTabs:
        self._automated_tab.click()
        return self

    @allure.step("Open Out of sync tab")
    def click_out_of_sync(self) -> NavigationTabs:
        self._out_of_sync_tab.click()
        return self

    @allure.step("Open Detached tab")
    def click_detached(self) -> NavigationTabs:
        self._detached_tab.click()
        return self

    @allure.step("Open Starred tab")
    def click_starred(self) -> NavigationTabs:
        self._starred_tab.click()
        return self

    @allure.step("Open display menu")
    def open_display(self) -> NavigationTabs:
        self._display_button.click()
        return self

    def link_by_name(self, name: str):
        return self._tabs_nav.get_by_role("link", name=name)

    def counter_by_name(self, name: str):
        return self.link_by_name(name).locator(".new-counter")

    @allure.step("Verify active tab is: {name}")
    def expect_tab_active(self, name: str) -> NavigationTabs:
        link = self.link_by_name(name)
        expect(link).to_be_visible()
        expect(link).to_have_class(re.compile(r"\bactive\b"))
        return self

    @allure.step("Verify tab {name} count is: {expected_count}")
    def expect_tab_count(self, name: str, expected_count: int) -> NavigationTabs:
        counter = self.counter_by_name(name)
        expect(counter).to_have_text(str(expected_count))
        return self
