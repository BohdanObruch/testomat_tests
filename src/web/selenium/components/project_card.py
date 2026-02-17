from __future__ import annotations

from enum import Enum

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ProjectCard:
    def __init__(self, card: WebElement):
        self.card = card
        self._link = card
        self._title = card.find_element(By.CSS_SELECTOR, "h3.text-gray-700")
        self._test_count = card.find_element(By.CSS_SELECTOR, "p.text-gray-500.text-sm")
        self._avatars = card.find_elements(By.CSS_SELECTOR, "img.rounded-full")
        self._badges = card.find_element(By.CSS_SELECTOR, ".project-badges")

    @property
    def title(self) -> str:
        return self._title.text.strip()

    @property
    def test_count(self) -> str:
        return self._test_count.text.strip()

    @property
    def href(self) -> str:
        return self._link.get_attribute("href")

    @allure.step("Verify project card has badge: {expected_badge}")
    def badges_has(self, expected_badge: Badges):
        assert expected_badge.value in self._badges.text, (
            f"Expected badge '{expected_badge.value}' not found in '{self._badges.text}'."
        )

    @allure.step("Open project card")
    def click(self):
        self._link.click()


class Badges(Enum):
    Demo = "Demo"
    Classical = "Classical"
    Pytest = "Pytest"
