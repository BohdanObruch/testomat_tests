# Testomat E2E Tests

Playwright-based end-to-end testing framework for [Testomat](https://testomat.io) application.

## Project Structure

```
testomat_tests/
├── src/                          # Source code
│   └── web/                      # Web UI automation
│       ├── application.py        # Application facade (entry point)
│       ├── helpers/              # Helpers/utilities
│       │   └── cookie_helper.py
│       ├── pages/                # Page Object Models
│       │   ├── home_page.py
│       │   ├── login_page.py
│       │   ├── new_projects_page.py
│       │   ├── project_page.py
│       │   └── projects_page.py
│       └── components/           # Reusable UI components
│           ├── add_test_menu.py
│           ├── navigation_tabs.py
│           ├── new_suite.py
│           ├── project_card.py
│           ├── projects_header.py
│           ├── side_bar.py
│           ├── suite.py
│           └── test_modal.py
│
├── tests/                        # Test suite
│   ├── conftest.py               # Pytest plugins
│   ├── fixtures/                 # Shared pytest fixtures
│   │   ├── config.py
│   │   ├── hooks.py
│   │   ├── playwright.py
│   │   └── settings.py
│   ├── first_test.py
│   └── web/                      # Web UI tests
│       ├── cookies_test.py
│       ├── login_page_test.py
│       ├── enterprise_plan/
│       │   ├── project_creation_test.py
│       │   ├── projects_page_test.py
│       │   ├── switch_company_test.py
│       │   └── test_create_suite.py
│       └── free_plan/
│           └── free_projects_test.py
│
├── test-result/                  # Test execution results
│   ├── report.html               # HTML report (pytest-html)
│   ├── screenshots/              # Screenshots on failure
│   ├── traces/                   # Playwright traces
│   ├── videos/                   # Video recordings
│   └── .auth/                    # Auth state storage
│
├── .env                          # Environment configuration
├── pyproject.toml                # Project configuration
└── uv.lock                       # Dependency lock file
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

# Run specific test file
pytest tests/web/login_page_test.py

# Generate HTML report (default: test-result/report.html)
pytest --html=test-result/report.html

# Override Playwright artifacts (defaults are set in pyproject.toml)
pytest --tracing=on --screenshot=on --video=on
```

## Test Markers

| Marker       | Description            |
|--------------|------------------------|
| `smoke`      | Quick validation tests |
| `regression` | Full test suite        |
| `web`        | Web UI specific tests  |
| `slow`       | Long-running tests     |

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

### Fixture Strategy

| Fixture            | Scope    | Purpose                            |
|--------------------|----------|------------------------------------|
| `configs`          | session  | Load environment variables         |
| `browser_instance` | session  | Reuse browser across tests         |
| `context`          | function | Fresh context per test             |
| `page`             | function | Fresh page per test                |
| `app`              | function | Application facade for fresh page  |
| `auth_state`       | session  | Cached authenticated storage state |
| `logged_context`   | function | Authenticated context per test     |
| `logged_app`       | function | Pre-authenticated page per test    |
| `free_project_app` | function | Auth state with empty company_id   |
| `shared_page`      | function | Shared page for parametrized tests |

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
- **python-dotenv** - Environment variable management

### Development

- **ruff** - Linter and formatter
