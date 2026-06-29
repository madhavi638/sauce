# conftest.py
"""
Pytest configuration and shared fixtures for the TC-83 test suite.

Fixtures
--------
driver (function-scoped)
    Initialises the WebDriver via DriverFactory, navigates to BASE_URL,
    yields the driver to the test, then quits the browser.

screenshot_on_failure (autouse, function-scoped)
    Automatically captures a PNG screenshot when a test fails and saves
    it to reports/screenshots/<test_name>_<timestamp>.png.
    The path is attached to the pytest HTML report via extra[] so it
    appears as an embedded image in the report.
"""

import os
import logging
import pytest

from utils.driver_factory import get_driver
from utils.config import BASE_URL, SCREENSHOT_DIR

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
#  WebDriver fixture                                                  #
# ------------------------------------------------------------------ #
@pytest.fixture(scope="function")
def driver():
    """
    Function-scoped WebDriver fixture.

    Lifecycle:
      setUp   → launch browser, maximise window, navigate to BASE_URL.
      yield   → hand driver to the test function.
      tearDown→ quit the browser unconditionally.
    """
    drv = get_driver()
    drv.maximize_window()
    logger.info(f"Browser launched. Navigating to BASE_URL: {BASE_URL}")
    drv.get(BASE_URL)
    yield drv
    logger.info("Tearing down: closing browser.")
    drv.quit()


# ------------------------------------------------------------------ #
#  Auto-screenshot on failure                                         #
# ------------------------------------------------------------------ #
@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, driver):
    """
    Autouse fixture — runs after every test.

    If the test FAILED, captures a screenshot, saves it to
    reports/screenshots/, and attaches it to the pytest-html report.
    """
    yield  # let the test run

    # Check if the test failed (rep.failed is set by pytest after yield)
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace(" ", "_")
        screenshot_path = f"{SCREENSHOT_DIR}/{test_name}_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        logger.error(f"Test FAILED — screenshot saved: {screenshot_path}")

        # Attach to pytest-html report
        if hasattr(request.node, "extras"):
            from pytest_html import extras as html_extras  # noqa: F401
            request.node.extras.append(
                {"name": "Screenshot", "format": "image", "content": screenshot_path}
            )


# ------------------------------------------------------------------ #
#  Hook: make test outcome available inside fixtures                  #
# ------------------------------------------------------------------ #
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Store the test phase result on the item so fixtures can inspect
    whether the test passed or failed.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
