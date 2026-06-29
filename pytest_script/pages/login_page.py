# pages/login_page.py
"""
LoginPage — Page Object for https://www.saucedemo.com login screen.

Inherits BasePage (Open/Closed principle):
  - Adds login-domain-specific locators and high-level actions.
  - BasePage is NOT modified to support new pages.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the Sauce Demo login page."""

    # ------------------------------------------------------------------ #
    #  Locators                                                            #
    # ------------------------------------------------------------------ #
    USERNAME_FIELD  = (By.ID, "user-name")
    PASSWORD_FIELD  = (By.ID, "password")
    LOGIN_BUTTON    = (By.ID, "login-button")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_TITLE = (By.CLASS_NAME, "title")
    APP_LOGO        = (By.CLASS_NAME, "login_logo")

    def __init__(self, driver):
        super().__init__(driver)

    # ------------------------------------------------------------------ #
    #  Navigation                                                          #
    # ------------------------------------------------------------------ #
    def open(self, url: str) -> None:
        """Navigate to the login page URL."""
        self.navigate_to(url)

    # ------------------------------------------------------------------ #
    #  Verification helpers                                                #
    # ------------------------------------------------------------------ #
    def is_login_page_displayed(self) -> bool:
        """
        Returns True when all login-page elements are visible:
        username field, password field, and login button.
        """
        return (
            self.is_element_visible(self.USERNAME_FIELD)
            and self.is_element_visible(self.PASSWORD_FIELD)
            and self.is_element_visible(self.LOGIN_BUTTON)
        )

    def is_dashboard_displayed(self) -> bool:
        """Returns True when the inventory/dashboard page title is visible."""
        return self.is_element_visible(self.INVENTORY_TITLE)

    def get_error_message(self) -> str:
        """Return the visible error message text, or empty string if none."""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.find_element(self.ERROR_MESSAGE).text
        return ""

    # ------------------------------------------------------------------ #
    #  Action methods                                                      #
    # ------------------------------------------------------------------ #
    def enter_username(self, username: str) -> None:
        """Type the given username into the username field."""
        self.enter_text(self.USERNAME_FIELD, username)

    def enter_password(self, password: str) -> None:
        """Type the given password into the password field."""
        self.enter_text(self.PASSWORD_FIELD, password)

    def click_login(self) -> None:
        """Click the Login button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """
        Convenience method: enter username, enter password, click Login.

        Args:
            username (str): Registered username.
            password (str): Corresponding password.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
