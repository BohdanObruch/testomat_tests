from playwright.sync_api import Page, expect


def test_login_with_invalid_creds(page:Page):
    open_home_page(page)

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    login_user(page, "newromka@gmail.com", "12345678")

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password.")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")


def test_search_project_in_company(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, "newromka@gmail.com", "ololo")

    target_project = 'python manufacture'
    search_for_project(page, target_project)

    expect(page.get_by_role("heading", name=target_project)).to_be_visible()


def test_should_be_possible_to_open_free_project(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, "newromka@gmail.com", "ololo")

    choose_free_project(page)

    target_project = 'python manufacture'
    search_for_project(page, target_project)

    expect(page.get_by_role("heading", name=target_project)).to_be_hidden()
    expect(page.get_by_text("You have not created any projects yet")).to_be_visible()


def test_can_not_create_project_without_company(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, "newromka@gmail.com", "ololo")

    choose_free_project(page)

    page.get_by_text("Create project").click()

    expect(page.get_by_text("Please switch to a company you own to create a project")).to_be_visible()


def test_change_view_projects_list_by_table_view(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, "newromka@gmail.com", "ololo")

    page.locator("#table-view").click()

    expect(page.locator("#table")).to_be_visible()
    expect(page.locator("#table-view")).to_contain_class("active_list_type")


def test_choose_project_by_classic_mode(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, "newromka@gmail.com", "ololo")

    click_create_project(page)

    expect(page.locator('#classical')).to_have_css('border-color', 'rgb(79, 70, 229)')
    expect(page.locator("#classical-img")).to_have_attribute("src", "/images/projects/circle-tick-dark-mode.svg")


def test_choose_project_by_bdd_mode(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, "newromka@gmail.com", "ololo")

    click_create_project(page)

    page.locator('#bdd').click()

    expect(page.locator('#bdd')).to_have_css('border-color', 'rgb(79, 70, 229)')
    expect(page.locator("#bdd-img")).to_have_attribute("src", "/images/projects/circle-tick-dark-mode.svg")


def test_can_create_project_by_header_button(page: Page):
    page.goto("https://app.testomat.io/users/sign_in")

    login_user(page, "newromka@gmail.com", "ololo")

    page.locator('.auth-header-nav [href="/projects/new"]').click()

    expect(page.locator(".common-page-header")).to_contain_text("New Project")
    expect(page.locator("#project_title")).to_be_visible()
    expect(page.get_by_role("button", name="Create", exact=True)).to_be_visible()


def click_create_project(page: Page):
    page.locator('[href="/projects/new"]').filter(has_text="Create").click()


def choose_free_project(page: Page):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")


def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()


def open_home_page(page: Page):
    page.goto("https://testomat.io")
