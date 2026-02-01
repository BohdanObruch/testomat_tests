from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage


class TestModal(BasePage):
    TITLE_INPUT = (By.CSS_SELECTOR, "[placeholder='Title']")
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def _heading(self, artifact_type: str):
        return (
            By.XPATH,
            f"//h3[contains(normalize-space(), '{artifact_type}')]",
        )

    def is_loaded(self, artifact_type: str):
        self.wait.for_visible(self._heading(f"New {artifact_type}"))
        self.wait.for_visible(self.TITLE_INPUT)
        return self

    def set_title(self, title: str):
        self.type_text(self.TITLE_INPUT, title)
        return self

    def save(self):
        self.click(self.SAVE_BUTTON)
        return self

    def edit_is_visible(self, artifact_type: str):
        self.wait.for_visible(self._heading(f"Edit {artifact_type}"))
        return self
