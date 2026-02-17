import allure
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Open login page")
    def open(self):
        self.page.goto("/users/sign_in")

    @allure.step("Verify login page is loaded")
    def is_loaded(self):
        expect(self.page.locator("#content-desktop form#new_user")).to_be_visible()

    def login_user(self, email: str, password: str, remember_me: bool = False):
        with allure.step("Login user with credentials"):
            allure.dynamic.parameter("email", "env.EMAIL")
            allure.dynamic.parameter("password", "env.PASSWORD")
            allure.dynamic.parameter("remember_me", remember_me)

            self.page.locator("#content-desktop #user_email").fill(email)
            self.page.locator("#content-desktop #user_password").fill(password)

            if remember_me:
                self.page.locator("#user_remember_me").check()

            self.page.get_by_role("button", name="Sign in").click()

    @allure.step("Verify invalid login message is visible")
    def invalid_login_message_visible(self):
        expect(self.page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
