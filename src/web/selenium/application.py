from __future__ import annotations

import allure
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.pages import LoginPage, NewProjectsPage, ProjectPage, ProjectsPage


class SeleniumApplication:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.login_page = LoginPage(driver)
        self.projects_page = ProjectsPage(driver, self.base_url)
        self.new_projects_page = NewProjectsPage(driver, self.base_url)
        self.project_page = ProjectPage(driver, self.base_url)

    def login(self, email: str, password: str):
        with allure.step("Login via Selenium application"):
            allure.dynamic.parameter("email", "env.EMAIL")
            allure.dynamic.parameter("password", "env.PASSWORD")
            self.login_page.open(self.base_url).is_loaded().login(email, password).should_see_success_message()
        return self
