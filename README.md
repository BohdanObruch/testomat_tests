# Testomat E2E Tests

Playwright-based end-to-end testing framework for [Testomat](https://testomat.io) application.

## Project Structure

```
testomat_tests/
|-- src/                          # Source code
|   |-- api/                      # API client + models
|   |   |-- client.py
|   |   |-- logger.py
|   |   |-- utils.py
|   |   |-- controllers/          # API endpoint controllers
|   |   |   |-- analytics.py
|   |   |   |-- attachment.py
|   |   |   |-- comment.py
|   |   |   |-- jira_issue.py
|   |   |   |-- permission.py
|   |   |   |-- plan.py
|   |   |   |-- project.py
|   |   |   |-- run.py
|   |   |   |-- rungroup.py
|   |   |   |-- settings.py
|   |   |   |-- step.py
|   |   |   |-- suite.py
|   |   |   |-- template.py
|   |   |   |-- test.py
|   |   |   |-- testrun.py
|   |   |   |-- timeline.py
|   |   |   |-- user.py
|   |   |   `-- user_project.py
|   |   `-- models/               # API response/request models
|   |       |-- jira_issue.py
|   |       |-- jira_issues.py
|   |       |-- plans.py
|   |       |-- project.py
|   |       |-- responses.py
|   |       |-- run.py
|   |       |-- run_group.py
|   |       |-- step.py
|   |       |-- suite.py
|   |       |-- template.py
|   |       |-- test.py
|   |       `-- test_run.py
|   `-- web/                      # Web UI automation
|       |-- application.py        # Application facade (entry point)
|       |-- helpers/              # Helpers/utilities
|       |   `-- cookie_helper.py
|       |-- pages/                # Page Object Models (Playwright)
|       |   |-- home_page.py
|       |   |-- login_page.py
|       |   |-- new_projects_page.py
|       |   |-- project_page.py
|       |   `-- projects_page.py
|       |-- components/           # Reusable UI components
|       |   |-- add_test_menu.py
|       |   |-- navigation_tabs.py
|       |   |-- new_suite.py
|       |   |-- project_card.py
|       |   |-- projects_header.py
|       |   |-- side_bar.py
|       |   |-- suite.py
|       |   `-- test_modal.py
|       `-- selenium/             # Selenium framework
|           |-- application.py
|           |-- core/
|           |   |-- base_page.py
|           |   `-- waits.py
|           |-- components/
|           |   |-- add_test_menu.py
|           |   |-- navigation_tabs.py
|           |   |-- new_suite.py
|           |   |-- project_card.py
|           |   |-- projects_header.py
|           |   |-- side_bar.py
|           |   |-- suite.py
|           |   `-- test_modal.py
|           `-- pages/
|               |-- login_page.py
|               |-- login_page_v2.py
|               |-- new_projects_page.py
|               |-- project_page.py
|               `-- projects_page.py
|
|-- tests/                        # Test suite
|   |-- conftest.py               # Pytest plugins
|   |-- fixtures/                 # Shared pytest fixtures
|   |   |-- api.py
|   |   |-- config.py
|   |   |-- hooks.py
|   |   |-- playwright.py
|   |   |-- selenium.py
|   |   `-- settings.py
|   |-- first_test.py
|   |-- api/                      # API tests
|   |   |-- projects_test.py
|   |   |-- suite_and_test_creation_test.py
|   |   |-- test_analytics.py
|   |   |-- test_misc.py
|   |   |-- test_plans.py
|   |   |-- test_runs.py
|   |   |-- test_suites.py
|   |   `-- test_templates.py
|   `-- web/                      # Web UI tests
|       |-- selenium/
|       |   |-- simple_selenium_test.py
|       |   `-- enterprise_plan/
|       |       |-- project_creation_test.py
|       |       |-- projects_page_test.py
|       |       |-- switch_company_test.py
|       |       |-- test_create_suite.py
|       |       `-- test_delete_project.py
|       |-- cookies_test.py
|       |-- login_page_test.py
|       |-- enterprise_plan/
|       |   |-- project_creation_test.py
|       |   |-- projects_page_test.py
|       |   |-- switch_company_test.py
|       |   `-- test_create_suite.py
|       `-- free_plan/
|           `-- free_projects_test.py
|
|-- test-result/                  # Test execution results
|   |-- report.html               # HTML report (pytest-html)
|   |-- screenshots/              # Screenshots on failure
|   |-- traces/                   # Playwright traces
|   |-- videos/                   # Video recordings
|   `-- .auth/                    # Auth state storage
|
|-- .env                          # Environment configuration
|-- pyproject.toml                # Project configuration
`-- uv.lock                       # Dependency lock file
```

## Requirements

- Python >= 3.14
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

## Installation

### Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Install Playwright browsers
uv run playwright install
```

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
playwright install
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
BASE_URL=https://testomat.io
BASE_APP_URL=https://app.testomat.io
EMAIL=your_email@example.com
PASSWORD=your_password
TESTOMAT_TOKEN=your_api_token
```

## Running Tests

```bash
# Run all tests
pytest

# Run smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run web UI tests
pytest -m web

# Run API tests
pytest -m api

# Run Selenium tests
pytest -m selenium

# Run specific test file
pytest tests/web/login_page_test.py

# Run specific Selenium test file
pytest tests/web/selenium/simple_selenium_test.py

# Generate HTML report (default: test-result/report.html)
pytest --html=test-result/report.html

# Override Playwright artifacts (defaults are set in pyproject.toml)
pytest --tracing=on --screenshot=on --video=on
```

## Test Markers

| Marker       | Description                 |
|--------------|-----------------------------|
| `smoke`      | Quick validation tests      |
| `regression` | Full test suite             |
| `web`        | Web UI specific tests       |
| `api`        | API tests using httpx       |
| `selenium`   | Selenium WebDriver UI tests |
| `slow`       | Long-running tests          |

## Architecture

### Page Object Model (POM)

Pages live in `src/web/pages` and are composed with reusable components from
`src/web/components`. Helper utilities are in `src/web/helpers`.

### Fluent Interface Pattern

Methods return `Self` for method chaining:

```python
app.login_page.open().is_loaded().login_user(email, password)
```

### Application Facade

The `Application` class provides a unified entry point to all pages:

```python
class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        # ...
```

### API Client + Models

API client lives in `src/api/client.py`, with response models in
`src/api/models`. API tests are under `tests/api` and use the `api_client`
fixture from `tests/fixtures/api.py` (JWT is cached per session).
Models are built with Pydantic.

### Selenium Page Objects

Selenium pages are in `src/web/selenium/pages` with shared waits and base
classes in `src/web/selenium/core`. Reusable UI components live in
`src/web/selenium/components`, and the Selenium entry point is
`src/web/selenium/application.py`. Selenium tests live in
`tests/web/selenium` (including the `enterprise_plan` suite) and use the
`driver` fixture from `tests/fixtures/selenium.py`.

### Selenium Application Facade

`SeleniumApplication` provides a single entry point to Selenium pages and
flows.

```python
def test_create_project_via_selenium(selenium_app):
    project_name = "Acme QA"
    (
        selenium_app.new_projects_page.open()
        .is_loaded()
        .fill_project_title(project_name)
        .click_create()
        .is_loaded_empty_project()
        .empty_project_name_is(project_name)
        .close_read_me()
    )
```

### Fixture Strategy

| Fixture                    | Scope    | Purpose                            |
|----------------------------|----------|------------------------------------|
| `configs`                  | session  | Load environment variables         |
| `browser_instance`         | session  | Reuse browser across tests         |
| `context`                  | function | Fresh context per test             |
| `page`                     | function | Fresh page per test                |
| `app`                      | function | Application facade for fresh page  |
| `auth_state`               | session  | Cached authenticated storage state |
| `logged_context`           | function | Authenticated context per test     |
| `logged_app`               | function | Pre-authenticated page per test    |
| `free_project_app`         | function | Auth state with empty company_id   |
| `shared_page`              | function | Shared page for parametrized tests |
| `api_client`               | session  | Authenticated API client (JWT)     |
| `driver`                   | function | Selenium WebDriver instance        |
| `selenium_app`             | function | Selenium app facade (logged in)    |
| `created_project_selenium` | function | New project via Selenium app       |

## Code Quality

The project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

```bash
# Check for linting issues
ruff check .

# Fix linting issues automatically
ruff check --fix .

# Format code
ruff format .
```

## Browser Configuration

Default browser settings (configured in `tests/fixtures/playwright.py`):

- Resolution: 1920x1080
- Locale: uk-UA
- Timezone: Europe/Kyiv
- Permissions: geolocation
- Headless: True
- Video recording: retain on failure (default in `pyproject.toml`)
- Screenshots: only on failure (default in `pyproject.toml`)
- Tracing: retain on failure (default in `pyproject.toml`)

## Dependencies

### Runtime

- **playwright** - Browser automation
- **pytest** - Test framework
- **pytest-html** - HTML reporting
- **pytest-playwright** - Playwright pytest integration
- **faker** - Test data generation
- **httpx** - API client
- **pydantic** - Data validation and API models
- **selenium** - Selenium WebDriver
- **python-dotenv** - Environment variable management

### Development

- **ruff** - Linter and formatter
