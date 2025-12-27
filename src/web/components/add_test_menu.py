from __future__ import annotations

import re

from playwright.sync_api import Page, expect


class AddTestMenu:
    def __init__(self, page: Page):
        self.page = page
        self._menu = self.page.locator("ul[data-ember-action]")

        self._folder_button = self._menu.get_by_role("button", name="Folder")
        self._suite_button = self._menu.get_by_role(
            "button",
            name=re.compile(r"^Suite\b"),
        )
        self._requirements_button = self._menu.get_by_role(
            "button",
            name="Tests From Requirement",
        )

        self._folder_description = self._menu.locator(
            "p",
            has_text="Collection of suites",
        )
        self._suite_description = self._menu.locator(
            "p",
            has_text="Collection of test cases",
        )
        self._requirements_description = self._menu.locator(
            "p",
            has_text="Use AI to generate tests from the requirement",
        )

    def is_loaded(self) -> AddTestMenu:
        expect(self._menu).to_be_visible()
        expect(self._folder_button).to_be_visible()
        expect(self._suite_button).to_be_visible()
        expect(self._requirements_button).to_be_visible()
        return self

    def expect_descriptions(self) -> AddTestMenu:
        expect(self._folder_description).to_be_visible()
        expect(self._suite_description).to_be_visible()
        expect(self._requirements_description).to_be_visible()
        return self

    def click_folder(self) -> AddTestMenu:
        self._folder_button.click()
        return self

    def click_suite(self) -> AddTestMenu:
        self._suite_button.click()
        return self

    def click_tests_from_requirement(self) -> AddTestMenu:
        self._requirements_button.click()
        return self
