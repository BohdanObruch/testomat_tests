from __future__ import annotations

from playwright.sync_api import Page, expect

from src.web.components import NewSuite


class Suite(NewSuite):
    def __init__(self, page: Page):
        super().__init__(page)

        self._suite_name = self._content.locator(".edit-in-place")
        self._detail_view = self._header.locator(".breadcrumbs")
        self._suite_id_link = self._detail_view.locator("a.copy-id")
        self._copy_id_button = self._detail_view.locator("button")

        self._pick_emoji_button = self._header.get_by_role(
            "button",
            name="Pick Emoji",
        )
        self._new_test_link = self._header.get_by_role("link", name="New Test")
        self._edit_link = self._header.get_by_role("link", name="Edit")
        self._comments_link = self._header.locator("a[href*='/comments']")
        self._header_more_actions_trigger = self._header.locator(
            ".ember-basic-dropdown-trigger",
        )

        self._convert_to_folder_link = self._content.get_by_role(
            "link",
            name="Convert to folder",
        )
        self._assign_dropdown = self._content.locator(
            ".assign-to .ember-basic-dropdown-trigger",
        )
        self._attach_requirements_link = self._content.get_by_role(
            "link",
            name="Attach Requirements",
        )

        self._description_tab = self._content.get_by_role(
            "tab",
            name="Description",
        )
        self._tests_tab = self._content.get_by_role("tab", name="Tests")
        self._attachments_tab = self._content.get_by_role(
            "tab",
            name="Attachments",
        )

        self._suggest_tests_button = self._content.get_by_role(
            "button",
            name="Suggest Tests",
        )
        self._suggest_tests_menu_button = self._content.locator(
            ".ai-btn.btn-only-icon",
        )
        self._tests_list = self._content.locator(".dragSortList.sidebar")
        self._add_test_input = self._content.locator("#item-title")
        self._create_test_button = self._content.get_by_role(
            "button",
            name="Create",
        )
        self._bulk_toggle = self._content.get_by_role("switch")

    def is_loaded(self) -> Suite:
        expect(self._panel).to_be_visible()
        expect(self._header).to_be_visible()
        expect(self._save_button).to_be_visible()
        expect(self._content).to_be_visible()
        expect(self._suite_title_input).to_be_visible()
        expect(self._editor).to_be_visible()
        return self

    def suite_name_is(self, expected_name: str) -> Suite:
        expect(self._suite_name).to_have_text(expected_name)
        return self

    def breadcrumbs_has(self, expected_text: str) -> Suite:
        expect(self._suite_id_link).to_have_text(expected_text)
        return self

    def click_copy_id(self) -> Suite:
        self._copy_id_button.click()
        return self

    def click_pick_emoji(self) -> Suite:
        self._pick_emoji_button.click()
        return self

    def click_new_test(self) -> Suite:
        self._new_test_link.click()
        return self

    def click_edit(self) -> Suite:
        self._edit_link.click()
        return self

    def click_comments(self) -> Suite:
        self._comments_link.click()
        return self

    def open_header_more_actions(self) -> Suite:
        self._header_more_actions_trigger.click()
        return self

    def click_convert_to_folder(self) -> Suite:
        self._convert_to_folder_link.click()
        return self

    def open_assign_dropdown(self) -> Suite:
        self._assign_dropdown.click()
        return self

    def click_attach_requirements(self) -> Suite:
        self._attach_requirements_link.click()
        return self

    def open_description_tab(self) -> Suite:
        self._description_tab.click()
        return self

    def open_tests_tab(self) -> Suite:
        self._tests_tab.click()
        return self

    def tab_name_is_active(self, tab_name: str) -> Suite:
        expect(self.page.get_by_role("tab", name=tab_name)).to_contain_class("ember-tabs__tab--selected")
        return self

    def open_attachments_tab(self) -> Suite:
        self._attachments_tab.click()
        return self

    def click_suggest_tests(self) -> Suite:
        self._suggest_tests_button.click()
        return self

    def open_suggest_tests_menu(self) -> Suite:
        self._suggest_tests_menu_button.click()
        return self

    def fill_new_test_title(self, title: str) -> Suite:
        self._add_test_input.fill(title)
        return self

    def click_create_test(self) -> Suite:
        self._create_test_button.click()
        return self

    def toggle_bulk(self) -> Suite:
        self._bulk_toggle.click()
        return self
