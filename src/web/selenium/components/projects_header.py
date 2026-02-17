from __future__ import annotations

import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

from src.web.selenium.core.base_page import BasePage


class ProjectsHeader(BasePage):
    PAGE_TITLE = (By.XPATH, "//h2[normalize-space()='Projects']")
    ENTERPRISE_PLAN_LABEL = (By.XPATH, "//*[text()[normalize-space()='Enterprise plan']]")
    FREE_PLAN_LABEL = (By.XPATH, "//*[text()[normalize-space()='free plan']]")
    COMPANY_SELECTOR = (By.CSS_SELECTOR, "#company_id")
    PLAN_BADGE = (By.CSS_SELECTOR, ".tooltip-project-plan")

    SEARCH_INPUT = (By.CSS_SELECTOR, "#search")

    CREATE_BUTTON = (By.XPATH, "//a[contains(@class,'common-btn-primary') and contains(normalize-space(), 'Create')]")
    MANAGE_BUTTON = (By.XPATH, "//a[contains(@class,'common-btn-secondary') and normalize-space()='Manage']")

    GRID_VIEW_BUTTON = (By.CSS_SELECTOR, "#grid-view")
    TABLE_VIEW_BUTTON = (By.CSS_SELECTOR, "#table-view")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step("Select company: {company_name}")
    def select_company(self, company_name: str):
        selector = Select(self.find(self.COMPANY_SELECTOR))
        selector.select_by_visible_text(company_name)
        return self

    @allure.step("Search project: {query}")
    def search_project(self, query: str):
        self.type_text(self.SEARCH_INPUT, query)
        return self

    @allure.step("Click create project")
    def click_create(self):
        self.click(self.CREATE_BUTTON)
        return self

    @allure.step("Click manage projects")
    def click_manage(self):
        self.click(self.MANAGE_BUTTON)
        return self

    @allure.step("Switch to grid view")
    def switch_to_grid_view(self):
        self.click(self.GRID_VIEW_BUTTON)
        return self

    @allure.step("Switch to table view")
    def switch_to_table_view(self):
        self.click(self.TABLE_VIEW_BUTTON)
        return self

    @allure.step("Verify selected company is: {expected_value}")
    def check_selected_company(self, expected_value: str):
        selector = Select(self.find(self.COMPANY_SELECTOR))
        assert selector.first_selected_option.text.strip() == expected_value
        return self

    @allure.step("Verify plan name is: {expected_value}")
    def plan_name_should_be(self, expected_value: str):
        badge = self.find(self.PLAN_BADGE)
        span = badge.find_element(By.CSS_SELECTOR, "span")
        assert span.text.strip() == expected_value
        return self

    @allure.step("Hover free plan label")
    def hover_free_plan_label(self):
        element = self.find(self.FREE_PLAN_LABEL)
        ActionChains(self.driver).move_to_element(element).perform()
        return self
