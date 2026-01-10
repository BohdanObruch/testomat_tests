from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pytest


@dataclass(frozen=True)
class PlaywrightSettings:
    screenshot: Optional[str]
    video: Optional[str]
    tracing: Optional[str]
    output_dir: Path
    screenshot_dir: Path
    video_dir: Path
    trace_dir: Path


def _get_option(config: pytest.Config, name: str) -> Optional[str]:
    try:
        return config.getoption(name)
    except Exception:
        return None


@pytest.fixture(scope="session")
def playwright_settings(request: pytest.FixtureRequest) -> PlaywrightSettings:
    output_dir = Path(request.config.rootpath) / "test-result"
    return PlaywrightSettings(
        screenshot=_get_option(request.config, "screenshot"),
        video=_get_option(request.config, "video"),
        tracing=_get_option(request.config, "tracing"),
        output_dir=output_dir,
        screenshot_dir=output_dir / "screenshots",
        video_dir=output_dir / "videos",
        trace_dir=output_dir / "traces",
    )
