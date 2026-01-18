from playwright.sync_api import Page, expect

from src.web.components import ProjectCard, ProjectsHeader


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = ProjectsHeader(page)

        self.success_message = page.locator(".common-flash-success-right p")
        self.info_message = page.locator(".common-flash-info-right p")

        self.projects_grid = page.locator("#grid")
        self._project_cards = page.locator('#grid ul li a[href*="/projects/"]')
        self.table = page.locator("#table")
        self.empty_projects_message = page.get_by_text("You have not created any projects yet")
        self.new_project_link = page.locator('.auth-header-nav [href="/projects/new"]')

        self.total_count = page.locator(".common-counter")

    def navigate(self, url: str = "/projects"):
        self.page.goto(url)

    def get_success_message(self) -> str:
        return self.success_message.text_content().strip()

    def get_projects(self) -> list[ProjectCard]:
        return [ProjectCard(card) for card in self._project_cards.all()]

    def get_project_by_title(self, title: str) -> ProjectCard:
        card = self._project_cards.filter(has=self.page.locator("h3", has_text=title)).first
        return ProjectCard(card)

    def click_project_by_title(self, title: str):
        card = self._project_cards.filter(has=self.page.locator("h3", has_text=title)).first
        card.click()
        return self

    def count_of_project_visible(self, expected_count: int):
        return expect(self._project_cards.filter(visible=True)).to_have_count(expected_count)

    def get_total_projects(self) -> int:
        return int(self.total_count.text_content())

    def search_and_get_results(self, query: str) -> list[ProjectCard]:
        self.header.search_project(query)
        self.page.wait_for_timeout(300)
        return self.get_projects()

    def verify_page_loaded(self):
        expect(self.header.page_title).to_be_visible()
        expect(self.projects_grid).to_be_visible()

    def verify_success_message(self, expected_text: str):
        expect(self.success_message).to_have_text(expected_text)

    def expect_project_heading_hidden(self, title: str):
        expect(self.page.get_by_role("heading", name=title)).to_be_hidden()

    def expect_no_projects_message(self):
        expect(self.empty_projects_message).to_be_visible()

    def expect_info_message(self, expected_text: str):
        expect(self.info_message).to_have_text(expected_text)

    def expect_tooltip_message(self, expected_text: str):
        expect(self.page.get_by_text(expected_text)).to_be_visible()

    def expect_table_view_active(self):
        expect(self.table).to_be_visible()
        expect(self.header.table_view_button).to_contain_class("active_list_type")

    def open_new_project_from_header(self):
        self.new_project_link.click()

    def is_loaded(self):
        expect(self.page.locator(".common-flash-success")).to_be_visible()
        expect(self.page.locator(".common-flash-success")).to_have_text("Signed in successfully")

        expect(self.page.locator(".common-flash-success", has_text="Signed in successfully")).to_be_visible()
