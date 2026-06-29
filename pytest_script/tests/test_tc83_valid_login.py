# tests/test_tc83_valid_login.py
"""
TC-83: Successful Login with Valid Username and Password
========================================================
Description : Verify that a registered user can successfully log in to
              https://www.saucedemo.com using a valid username and password.
              Linked to SAUC-3.

Priority    : High
Test Data   : validdata.xlsx → Row 2 → standard_user / secret_sauce

Test Steps  :
  Step 1 → Navigate to login page; verify all required elements are displayed.
  Step 2 → Enter a valid registered username; verify it is accepted.
  Step 3 → Enter the corresponding valid password; verify it is masked and accepted.
  Step 4 → Click the Login button; verify the user is redirected to the dashboard.

Reporting   : pytest-html report → reports/pytest_script.html
Screenshots : Auto-captured on failure → reports/screenshots/<test>_<ts>.png
"""

import pytest
import logging

from pages.login_page import LoginPage
from utils.data_reader import read_valid_credentials
from utils.config import BASE_URL

logger = logging.getLogger(__name__)


class TestTC83ValidLogin:
    """
    Test class for TC-83 — Successful Login with Valid Username and Password.

    Each test method covers one Step defined in qTest, plus a full E2E flow.
    Screenshots are captured automatically on failure via the autouse fixture
    defined in conftest.py.
    """

    # ================================================================== #
    #  Step 1 — Navigate to login page                                    #
    # ================================================================== #
    def test_step1_login_page_is_displayed(self, driver):
        """
        Step 1: Navigate to the application login page.
        Expected: Login page displayed with username field, password field,
                  and Login button all visible.
        """
        login_page = LoginPage(driver)
        login_page.open(BASE_URL)

        assert login_page.is_login_page_displayed(), (
            "STEP 1 FAILED: Login page elements (username, password, login button) "
            "were not all visible after navigating to the app URL."
        )
        logger.info(
            "✅ Step 1 PASSED: Login page displayed with all required elements "
            f"at {driver.current_url}"
        )

    # ================================================================== #
    #  Step 2 — Enter valid username                                      #
    # ================================================================== #
    def test_step2_enter_valid_username(self, driver):
        """
        Step 2: Enter a valid registered username.
        Expected: Username is accepted and visible in the input field.
        """
        username, _ = read_valid_credentials("validdata.xlsx", row=2)
        login_page = LoginPage(driver)
        login_page.open(BASE_URL)
        login_page.enter_username(username)

        actual_value = driver.find_element(*LoginPage.USERNAME_FIELD).get_attribute("value")
        assert actual_value == username, (
            f"STEP 2 FAILED: Expected username field to contain '{username}', "
            f"but got '{actual_value}'."
        )
        logger.info(f"✅ Step 2 PASSED: Username '{username}' entered and verified in field.")

    # ================================================================== #
    #  Step 3 — Enter valid password (masked)                             #
    # ================================================================== #
    def test_step3_enter_valid_password(self, driver):
        """
        Step 3: Enter the corresponding valid password.
        Expected: Password field is of type='password' (masked) and value is accepted.
        """
        username, password = read_valid_credentials("validdata.xlsx", row=2)
        login_page = LoginPage(driver)
        login_page.open(BASE_URL)
        login_page.enter_username(username)
        login_page.enter_password(password)

        pwd_field  = driver.find_element(*LoginPage.PASSWORD_FIELD)
        field_type = pwd_field.get_attribute("type")
        pwd_value  = pwd_field.get_attribute("value")

        assert field_type == "password", (
            f"STEP 3 FAILED: Password field type should be 'password' (masked), "
            f"got '{field_type}'."
        )
        assert pwd_value == password, (
            f"STEP 3 FAILED: Password field value mismatch — "
            f"expected '{password}', got '{pwd_value}'."
        )
        logger.info(
            "✅ Step 3 PASSED: Password field is masked (type='password') "
            "and value entered correctly."
        )

    # ================================================================== #
    #  Step 4 — Click Login → redirect to dashboard                       #
    # ================================================================== #
    def test_step4_successful_login_redirects_to_dashboard(self, driver):
        """
        Step 4: Click the Login button.
        Expected: User is redirected to the dashboard/inventory page.
                  URL contains 'inventory' and the page title element is visible.
        """
        username, password = read_valid_credentials("validdata.xlsx", row=2)
        login_page = LoginPage(driver)
        login_page.open(BASE_URL)
        login_page.login(username, password)

        assert login_page.is_dashboard_displayed(), (
            "STEP 4 FAILED: Dashboard/inventory page title was not visible "
            "after clicking Login with valid credentials."
        )
        assert "inventory" in driver.current_url, (
            f"STEP 4 FAILED: Expected 'inventory' in the post-login URL, "
            f"but got: {driver.current_url}"
        )
        logger.info(
            f"✅ Step 4 PASSED: User '{username}' successfully redirected to dashboard. "
            f"Current URL: {driver.current_url}"
        )

    # ================================================================== #
    #  E2E — Full TC-83 Flow                                              #
    # ================================================================== #
    def test_e2e_tc83_full_login_flow(self, driver):
        """
        E2E: TC-83 Full Flow — Step 1 through Step 4 in a single test.

        Pipeline:
          1. Navigate to the login page → verify page displayed.
          2. Enter valid username (standard_user) from validdata.xlsx.
          3. Enter valid password (secret_sauce) from validdata.xlsx.
          4. Click Login → assert dashboard visible + URL contains 'inventory'.

        Test Data Source: validdata.xlsx (Row 2) → standard_user / secret_sauce
        """
        username, password = read_valid_credentials("validdata.xlsx", row=2)
        logger.info(f"[TC-83 E2E] Test data loaded → username: '{username}'")

        login_page = LoginPage(driver)

        # ── Step 1: Navigate ──────────────────────────────────────────
        login_page.open(BASE_URL)
        assert login_page.is_login_page_displayed(), (
            "[TC-83 E2E] FAILED at Step 1: Login page not displayed correctly."
        )
        logger.info("[TC-83 E2E] Step 1 ✅ Login page visible.")

        # ── Step 2: Enter username ────────────────────────────────────
        login_page.enter_username(username)
        logger.info(f"[TC-83 E2E] Step 2 ✅ Username '{username}' entered.")

        # ── Step 3: Enter password ────────────────────────────────────
        login_page.enter_password(password)
        logger.info("[TC-83 E2E] Step 3 ✅ Password entered (masked field).")

        # ── Step 4: Click login, verify dashboard ─────────────────────
        login_page.click_login()

        assert login_page.is_dashboard_displayed(), (
            "[TC-83 E2E] FAILED at Step 4: Dashboard not displayed after valid login."
        )
        assert "inventory" in driver.current_url, (
            f"[TC-83 E2E] FAILED at Step 4: URL does not contain 'inventory'. "
            f"Got: {driver.current_url}"
        )
        logger.info(
            f"[TC-83 E2E] Step 4 ✅ Dashboard confirmed. "
            f"URL: {driver.current_url}"
        )
        logger.info("✅ TC-83 E2E PASSED — Full successful login flow completed.")
