from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Generator, Optional, TYPE_CHECKING

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, ViewportSize, sync_playwright

from fixtures.config import Config
from src.web.application import Application

if TYPE_CHECKING:
    from fixtures.settings import PlaywrightSettings


def clear_browser_state(page: Page) -> None:
    """Clear cookies and local storage for the current page context."""
    page.context.clear_cookies()
    clear_page_storage(page)


def clear_page_storage(page: Page) -> None:
    """Clear local/session storage without touching cookies."""
    page.evaluate("window.localStorage.clear()")
    page.evaluate("window.sessionStorage.clear()")


def _test_failed(request: pytest.FixtureRequest) -> bool:
    rep_call = getattr(request.node, "rep_call", None)
    return bool(rep_call and rep_call.failed)


def _normalized_option(value: Optional[str]) -> str:
    return (value or "off").lower()


def _option_enabled(
        option: Optional[str],
        *,
        on_value: str,
        on_failure_value: str,
        request: pytest.FixtureRequest,
) -> bool:
    normalized = _normalized_option(option)
    if normalized == on_value:
        return True
    if normalized == on_failure_value:
        return _test_failed(request)
    return False


def _should_take_screenshot(settings: PlaywrightSettings, request: pytest.FixtureRequest) -> bool:
    return _option_enabled(
        settings.screenshot,
        on_value="on",
        on_failure_value="only-on-failure",
        request=request,
    )


def _artifact_basename(request: pytest.FixtureRequest, browser_name: str) -> str:
    module_name = Path(str(request.node.fspath)).stem
    name = f"{module_name}__{request.node.name}"
    name = name.replace("/", "_").replace("\\", "_")
    if f"[{browser_name}]" not in name:
        name = f"{name}[{browser_name}]"
    return name


def _browser_name_from_context(context: BrowserContext) -> str:
    try:
        return context.browser.browser_type.name
    except Exception:
        return "chromium"


def _capture_screenshot(page: Page, request: pytest.FixtureRequest, settings: PlaywrightSettings) -> None:
    if not _should_take_screenshot(settings, request):
        return
    settings.screenshot_dir.mkdir(parents=True, exist_ok=True)
    browser_name = _browser_name_from_context(page.context)
    path = settings.screenshot_dir / f"{_artifact_basename(request, browser_name)}.png"
    try:
        page.screenshot(path=str(path), full_page=True)
    except Exception:
        pass


def _finalize_page(page: Page, request: pytest.FixtureRequest, settings: PlaywrightSettings) -> None:
    _capture_screenshot(page, request, settings)
    video = page.video
    page.close()
    _cleanup_video(video, request, settings, _browser_name_from_context(page.context))


def _video_should_keep(settings: PlaywrightSettings, request: pytest.FixtureRequest) -> bool:
    return _option_enabled(
        settings.video,
        on_value="on",
        on_failure_value="retain-on-failure",
        request=request,
    )


def _retry_on_permission(action, *, retries: int = 3, delay: float = 0.2) -> bool:
    for _ in range(retries):
        try:
            action()
            return True
        except PermissionError:
            time.sleep(delay)
        except FileNotFoundError:
            return False
        except Exception:
            return False
    return False


def _save_video(video, target: Path) -> bool:
    return _retry_on_permission(lambda: video.save_as(path=str(target)))


def _cleanup_video(
        video,
        request: pytest.FixtureRequest,
        settings: PlaywrightSettings,
        browser_name: str,
) -> None:
    if not video:
        return
    try:
        path = Path(video.path())
    except Exception:
        return
    if not _video_should_keep(settings, request):
        _retry_on_permission(lambda: os.remove(path))
        return
    settings.video_dir.mkdir(parents=True, exist_ok=True)
    target = settings.video_dir / f"{_artifact_basename(request, browser_name)}.webm"
    if target == path:
        return
    if _save_video(video, target):
        try:
            os.remove(path)
        except Exception:
            pass
        return
    _retry_on_permission(lambda: os.replace(path, target))


def _should_trace(settings: PlaywrightSettings, request: pytest.FixtureRequest) -> bool:
    return _option_enabled(
        settings.tracing,
        on_value="on",
        on_failure_value="retain-on-failure",
        request=request,
    )


def _start_tracing(context: BrowserContext, settings: PlaywrightSettings) -> None:
    option = _normalized_option(settings.tracing)
    if option not in {"on", "retain-on-failure"}:
        return
    context.tracing.start(screenshots=True, snapshots=True, sources=True)


def _stop_tracing(
        context: BrowserContext,
        request: pytest.FixtureRequest,
        settings: PlaywrightSettings,
) -> None:
    option = _normalized_option(settings.tracing)
    if option not in {"on", "retain-on-failure"}:
        return
    if not _should_trace(settings, request):
        context.tracing.stop()
        return
    settings.trace_dir.mkdir(parents=True, exist_ok=True)
    browser_name = _browser_name_from_context(context)
    path = settings.trace_dir / f"{_artifact_basename(request, browser_name)}.zip"
    context.tracing.stop(path=str(path))


def build_browser_context(
        browser_instance: Browser,
        configs: Config,
        settings: PlaywrightSettings,
        *,
        enable_video: bool = True,
        storage_state: Optional[Path] = None,
) -> BrowserContext:
    viewport: ViewportSize = {"width": 1920, "height": 1080}
    context_kwargs = {
        "base_url": configs.app_base_url,
        "viewport": viewport,
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "permissions": ["geolocation"],
    }
    if storage_state is not None:
        context_kwargs["storage_state"] = str(storage_state)
    if enable_video and _normalized_option(settings.video) in {"on", "retain-on-failure"}:
        settings.video_dir.mkdir(parents=True, exist_ok=True)
        context_kwargs["record_video_dir"] = str(settings.video_dir)
    return browser_instance.new_context(**context_kwargs)


@pytest.fixture(scope="session")
def browser_instance() -> Generator[Browser, None, None]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=0, timeout=30000)
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def auth_state(
        browser_instance: Browser,
        configs: Config,
        playwright_settings: PlaywrightSettings,
) -> Path:
    auth_path = playwright_settings.output_dir / "auth_state.json"
    auth_path.parent.mkdir(parents=True, exist_ok=True)
    context = build_browser_context(browser_instance, configs, playwright_settings, enable_video=False)
    page = context.new_page()
    app = Application(page)
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    context.storage_state(path=str(auth_path))
    page.close()
    context.close()
    return auth_path


# 1. Clean app - fresh page per test (function scope)
@pytest.fixture(scope="function")
def context(
        browser_instance: Browser,
        configs: Config,
        playwright_settings: PlaywrightSettings,
        request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    context = build_browser_context(browser_instance, configs, playwright_settings)
    _start_tracing(context, playwright_settings)
    try:
        yield context
    finally:
        _stop_tracing(context, request, playwright_settings)
        context.close()


@pytest.fixture(scope="function")
def page(
        context: BrowserContext,
        request: pytest.FixtureRequest,
        playwright_settings: PlaywrightSettings,
) -> Generator[Page, None, None]:
    page = context.new_page()
    try:
        yield page
    finally:
        _finalize_page(page, request, playwright_settings)


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


# 2. Logged app - isolated context per test with shared auth state
@pytest.fixture(scope="function")
def logged_context(
        browser_instance: Browser,
        configs: Config,
        playwright_settings: PlaywrightSettings,
        auth_state: Path,
        request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    context = build_browser_context(
        browser_instance,
        configs,
        playwright_settings,
        storage_state=auth_state,
    )
    _start_tracing(context, playwright_settings)
    try:
        yield context
    finally:
        _stop_tracing(context, request, playwright_settings)
        context.close()


@pytest.fixture(scope="function")
def logged_app(
        logged_context: BrowserContext,
        request: pytest.FixtureRequest,
        playwright_settings: PlaywrightSettings,
) -> Generator[Application, None, None]:
    page = logged_context.new_page()
    try:
        yield Application(page)
    finally:
        _finalize_page(page, request, playwright_settings)


# 3. Shared context for parametrized tests (module scope)
@pytest.fixture(scope="module")
def shared_browser(
        browser_instance: Browser,
        configs: Config,
        playwright_settings: PlaywrightSettings,
) -> Generator[BrowserContext, None, None]:
    context = build_browser_context(browser_instance, configs, playwright_settings)
    yield context
    context.close()


@pytest.fixture(scope="function")
def shared_page(
        shared_browser: BrowserContext,
        request: pytest.FixtureRequest,
        playwright_settings: PlaywrightSettings,
) -> Generator[Application, None, None]:
    page = shared_browser.new_page()
    _start_tracing(shared_browser, playwright_settings)
    try:
        yield Application(page)
    finally:
        _stop_tracing(shared_browser, request, playwright_settings)
        clear_browser_state(page)
        _finalize_page(page, request, playwright_settings)
