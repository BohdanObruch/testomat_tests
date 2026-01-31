from playwright.sync_api import Page

from src import HomePage, LoginPage, NewProjectsPage, ProjectPage, ProjectsPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        self.new_projects_page = NewProjectsPage(page)
        self.project_page = ProjectPage(page)
