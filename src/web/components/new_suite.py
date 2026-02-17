from __future__ import annotations

import allure
from playwright.sync_api import Page, expect


class NewSuite:
    def __init__(self, page: Page):
        self.page = page

        self._panel = page.locator(".detail")
        self._resizer = self._panel.locator(".resizer")
        self._back_close_button = self._panel.locator(".back")

        self._header = self._panel.locator(".detail-view-header")
        self._save_button = self._panel.get_by_role("button", name="Save")
        self._save_dropdown_trigger = self._save_button.locator(
            "xpath=following-sibling::div[contains(@class,'ember-basic-dropdown-trigger')]"
        )
        self._cancel_link = self._panel.get_by_role("link", name="Cancel")
        self._header_close_button = self._panel.locator(
            ".detail-view-actions .third-btn",
        )

        self._content = self._panel.locator(".detail-view-content")
        self._title = self._content.get_by_role("heading", name="New Suite")
        self._creates_in = self._content.locator("span", has_text="Creates in:Root")
        self._edit_location_button = self._content.locator(
            "button .md-icon-pencil",
        )
        self._set_labels_link = self._content.get_by_role("link", name="Set labels")
        self._shortcut_icon = self._content.locator(".keyboard-shortcut-icon")

        self._suite_title_label = self._content.get_by_text(
            "Title of a suite",
            exact=True,
        )
        self._suite_title_input = self._content.locator(
            'input[placeholder="Title"]',
        )

        self._toolbar = self._content.locator("ul.form-test")
        self._preview_button = self._content.get_by_role("button", name="Preview")
        self._attachments_button = self._content.get_by_role(
            "button",
            name="Attachments",
        )
        self._more_actions_trigger = self._content.locator(
            ".ember-basic-dropdown-trigger .md-icon",
        )

        self._editor = self._content.locator(
            ".editor-suite",
        )
        self._editor_frame = self._editor.frame_locator("iframe")
        self._description_input = self._editor_frame.locator("textarea.inputarea")
        self.suite_checkboxes = page.locator(".tree-branch")  # .tree-branch input

    @allure.step("Verify new suite selector is loaded")
    def is_loaded(self) -> NewSuite:
        expect(self.page.get_by_role("heading", name="Select suite for test")).to_be_visible()
        expect(self.suite_checkboxes.first).to_be_visible()
        return self

    @allure.step("Select first suite")
    def select_first_suite(self) -> NewSuite:
        self.suite_checkboxes.first.click()
        self.page.get_by_role("button", name="Select").click()
        return self

    @allure.step("Set suite title: {title}")
    def set_suite_title(self, title: str) -> NewSuite:
        self._suite_title_input.fill(title)
        return self

    @allure.step("Save suite")
    def click_save(self) -> NewSuite:
        self._save_button.click()
        return self

    @allure.step("Open suite save menu")
    def open_save_menu(self) -> NewSuite:
        self._save_dropdown_trigger.click()
        return self

    @allure.step("Cancel suite editing")
    def click_cancel(self) -> NewSuite:
        self._cancel_link.click()
        return self

    @allure.step("Close suite panel with back button")
    def close_with_back_button(self) -> NewSuite:
        self._back_close_button.click()
        return self

    @allure.step("Close suite panel with header button")
    def close_with_header_button(self) -> NewSuite:
        self._header_close_button.click()
        return self

    @allure.step("Fill suite title: {title}")
    def fill_suite_title(self, title: str) -> NewSuite:
        self._suite_title_input.fill(title)
        return self

    @allure.step("Fill suite description")
    def fill_description(self, text: str) -> NewSuite:
        self._description_input.focus()
        self._description_input.fill(text)
        return self
