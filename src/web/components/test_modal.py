import allure
from playwright.sync_api import Page, expect


class TestModal:
    def __init__(self, page: Page):
        self.page = page
        self._title = page.locator("[placeholder='Title']")

    @allure.step("Verify test modal is loaded for: {artifact_type}")
    def is_loaded(self, artifact_type: str) -> TestModal:
        expect(self.page.get_by_role("heading ", name=f"New {artifact_type}")).to_be_visible()
        expect(self._title).to_be_visible()
        return self

    @allure.step("Set modal title: {title}")
    def set_title(self, title: str) -> TestModal:
        self._title.fill(title)
        return self

    @allure.step("Save modal")
    def save(self) -> TestModal:
        self.page.get_by_role("button", name="Save").click()
        return self

    @allure.step("Verify edit modal is visible for: {artifact_type}")
    def edit_is_visible(self, artifact_type: str) -> TestModal:
        expect(self.page.get_by_role("heading", name=f"Edit {artifact_type}")).to_be_visible()
        return self

    @allure.step("Verify saved status label is visible")
    def saved_status_label_visible(self) -> TestModal:
        expect(self.page.get_by_role("heading", name="Saved")).to_be_visible()
