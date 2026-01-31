from typing import Self

from playwright.sync_api import Page, expect

from src.web.components import AddTestMenu, NavigationTabs, NewSuite, SideBar, Suite, TestModal


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)
        self.navigation_tabs = NavigationTabs(page)
        self.test_menu = AddTestMenu(page)
        self.add_suite = Suite(page)
        self.test_modal = TestModal(page)
        self.suite = Suite(page)
        self.new_suite = NewSuite(page)
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
        self.settings_link = self.page.get_by_role("link").filter(has_text="Settings")
        self.project_menu_settings = self.page.locator(".subnav-menu-settings")
        self.administration_button = self.page.get_by_role("button", name="Administration")
        self.delete_project_text = self.page.get_by_text("Delete Project")
        self.delete_project_button = self.page.get_by_role("button", name="Delete Project")
        self.deletion_warning = self.page.locator(".warning").filter(has_text="Project will be deleted in few minutes")

    def open_by_id(self, project_id: str) -> Self:
        self.page.goto(f"/projects/{project_id}")
        return self

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

    def go_to_settings(self) -> Self:
        self.settings_link.click()
        expect(self.project_menu_settings).to_be_visible()
        return self

    def delete_project(self) -> Self:
        self.administration_button.click()
        self.page.on("dialog", lambda dialog: dialog.accept())
        self.administration_button.click()
        expect(self.delete_project_text).to_be_visible()
        self.delete_project_button.click()
        self.page.on("dialog", lambda dialog: dialog.accept())
        return self

    def verify_project_deletion_started(self) -> Self:
        expect(self.deletion_warning).to_be_visible()
        return self

    def create_test_suite_via_popup(self):
        self.page.locator(".md-icon-chevron-down").click()
        self.page.get_by_text("Collection of test cases").click()

    def suite_with_name_is_visible(self, test_suite_name: str):
        expect(self.page.locator(".suites-list-content").get_by_text(test_suite_name)).to_be_visible()

    def create_test_via_popup(self):
        self.page.locator(".sticky-header").get_by_role("button", name="Test  ", exact=True).click()
        return self

    def create_first_suite(self, target_suite_name: str):
        self.page.locator("[placeholder='First Suite']").fill(target_suite_name)
        suite_button = self.page.get_by_role("button", name="Suite")
        suite_button.click()
        expect(suite_button).to_be_hidden()
        return self
