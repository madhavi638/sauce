# pages/base_page.py
"""
BasePage — Single Responsibility: wraps raw Selenium WebDriver interactions
so that page objects and tests never call the driver directly.

SOLID principles applied:
  S — One responsibility: low-level driver wrappers only.
  O — Open for extension (LoginPage inherits without modification here).
  L — Subclasses can replace BasePage where BasePage is expected.
  I — Thin interface; only what pages actually need.
  D — Pages depend on this abstraction, not on concrete WebDriver calls.
"""

import os
import logging
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import EXPLICIT_WAIT, SCREENSHOT_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    # ------------------------------------------------------------------ #
    #  Navigation                                                          #
    # ------------------------------------------------------------------ #
    def navigate_to(self, url: str) -> None:
        """Navigate the browser to the given URL."""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    # ------------------------------------------------------------------ #
    #  Element interaction helpers                                         #
    # ------------------------------------------------------------------ #
    def find_element(self, locator):
        """Wait for and return a visible element."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator) -> None:
        """Wait for element to be clickable, then click it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        logger.info(f"Clicking element: {locator}")
        element.click()

    def enter_text(self, locator, text: str) -> None:
        """Clear an input field and type text into it."""
        element = self.find_element(locator)
        element.clear()
        logger.info(f"Entering text into {locator}: '{text}'")
        element.send_keys(text)

    # ------------------------------------------------------------------ #
    #  State / assertion helpers                                           #
    # ------------------------------------------------------------------ #
    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Return the current page <title>."""
        return self.driver.title

    def is_element_visible(self, locator) -> bool:
        """Return True if the element is visible within the explicit wait, else False."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    #  Screenshot helper                                                   #
    # ------------------------------------------------------------------ #
    def take_screenshot(self, test_name: str) -> str:
        """
        Capture a PNG screenshot and save it under SCREENSHOT_DIR.

        Args:
            test_name (str): Logical name used in the filename.

        Returns:
            str: Absolute path of the saved screenshot.
        """
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SCREENSHOT_DIR}/{test_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
        return filename
