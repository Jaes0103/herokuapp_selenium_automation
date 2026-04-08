"""
Test: Page Object Model (POM) Pattern
Site: https://the-internet.herokuapp.com (public demo site)
Tools: Selenium WebDriver, Python
Author: Jessca Belle Bagolor
Description:
    Demonstrates the Page Object Model design pattern — a best practice in
    automation that separates page structure from test logic, making tests
    easier to maintain and scale.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# ──────────────────────────────────────────────
# PAGE OBJECTS — define page structure here
# ──────────────────────────────────────────────

class LoginPage:
    """Encapsulates all interactions with the Login page."""

    URL = "https://the-internet.herokuapp.com/login"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def enter_username(self, username):
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys(username)
        return self

    def enter_password(self, password):
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)
        return self

    def click_login(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        return self

    def login(self, username, password):
        """Convenience method: full login flow in one call."""
        return self.enter_username(username).enter_password(password).click_login()

    def get_flash_message(self):
        message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        return message.text

    def is_error_displayed(self):
        try:
            element = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.error"))
            )
            return element.is_displayed()
        except Exception:
            return False


class SecurePage:
    """Encapsulates all interactions with the Secure Area page."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self):
        return "/secure" in self.driver.current_url

    def get_heading(self):
        heading = self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h2"))
        )
        return heading.text

    def logout(self):
        logout_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/logout']"))
        )
        logout_btn.click()
        return LoginPage(self.driver)


# ──────────────────────────────────────────────
# TEST CASES — clean, readable, no locators here
# ──────────────────────────────────────────────

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).open()


class TestLoginWithPOM:

    def test_valid_login_reaches_secure_page(self, login_page):
        """TC-001: Valid login navigates to the secure area."""
        login_page.login("tomsmith", "SuperSecretPassword!")
        secure_page = SecurePage(login_page.driver)

        assert secure_page.is_loaded()
        assert "Secure Area" in secure_page.get_heading()

    def test_invalid_login_shows_error(self, login_page):
        """TC-002: Invalid credentials should display an error message."""
        login_page.login("wronguser", "wrongpass")

        assert login_page.is_error_displayed()
        assert "invalid" in login_page.get_flash_message().lower()

    def test_logout_returns_to_login(self, login_page):
        """TC-003: Logging out should bring the user back to the login page."""
        login_page.login("tomsmith", "SuperSecretPassword!")
        secure_page = SecurePage(login_page.driver)

        returned_login_page = secure_page.logout()

        assert "You logged out" in returned_login_page.get_flash_message()
        assert login_page.driver.current_url == LoginPage.URL

    @pytest.mark.parametrize("username, password, expected_error", [
        ("tomsmith", "wrongpass", "password is invalid"),
        ("wronguser", "SuperSecretPassword!", "username is invalid"),
        ("", "", "username is invalid"),
    ])
    def test_login_error_messages(self, login_page, username, password, expected_error):
        """TC-004: Parametrized test for multiple invalid credential combinations."""
        login_page.login(username, password)

        assert login_page.is_error_displayed()
        assert expected_error in login_page.get_flash_message().lower()
