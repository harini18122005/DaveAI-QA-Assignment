import re
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1200")

    browser = webdriver.Chrome(options=options)
    try:
        browser.set_window_size(1440, 1200)
        browser.implicitly_wait(0)
        yield browser
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    screenshots_dir = PROJECT_ROOT / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    safe_test_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.nodeid)
    screenshot_path = screenshots_dir / f"{safe_test_name}.png"
    browser.save_screenshot(str(screenshot_path))