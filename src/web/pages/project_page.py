from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import SideBar, NavigationTabs, AddTestMenu, NewSuite, Suite


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)
        self.navigation_tabs = NavigationTabs(page)
        self.test_menu = AddTestMenu(page)
        self.add_suite = NewSuite(page)
        self.suite = Suite(page)
        self.header = self.page.locator(".sticky-header")
        self.navigation_menu = self.page.locator(".mainnav-menu")
        self.placeholder = self.page.locator("[placeholder='First Suite']")
        self.create_suite_button = self.page.get_by_role("button", name="Suite")
        self.add_test_button = self.page.get_by_role("button", name="Test", exact=True)
        self.add_test_dropdown = self.add_test_button.locator(
            "xpath=following-sibling::div[contains(@class,'ember-basic-dropdown')]"
        )  # self.add_test_button.locator("xpath=..").locator(".ember-basic-dropdown")
        self.empty_project_name = self.header.locator("h2")
        self.breadcrumbs_page = self.page.locator(".breadcrumbs-page")
        self.project_name = self.breadcrumbs_page.locator("a")
        self.readme_close_button = self.page.locator(".back .third-btn")
        self.suites = self.page.locator(".dragSortList")
        self.suite_item = self.suites.locator(".dragSortItem")
        self.suite_name = self.suite_item.locator(".ember-view span")

    def is_loaded_empty_project(self) -> Self:
        expect(self.header).to_be_visible(timeout=10_000)
        expect(self.navigation_menu).to_be_visible()
        expect(self.placeholder).to_be_visible()
        expect(self.create_suite_button).to_be_visible()
        return self

    def is_loaded_project(self) -> Self:
        expect(self.header).to_be_visible(timeout=10_000)
        expect(self.navigation_menu).to_be_visible()
        expect(self.add_test_button).to_be_visible()
        return self

    def empty_project_name_is(self, expected_project_name: str) -> Self:
        expect(self.empty_project_name).to_have_text(expected_project_name)
        return self

    def project_name_is(self, expected_project_name: str) -> Self:
        expect(self.project_name).to_have_text(expected_project_name.capitalize())
        return self

    def close_read_me(self) -> Self:
        self.readme_close_button.click()

    def click_add_test(self) -> Self:
        self.add_test_button.click()
        return self

    def open_add_test_dropdown(self) -> Self:
        self.add_test_dropdown.click()
        return self

    def verify_suite_is_present(self, suite_name: str) -> Self:
        all_suites = self.suite_name.all_inner_texts()
        assert suite_name in all_suites, f"Suite '{suite_name}' not found in project."
        return self
