"""
Selenium Test: Login Flow Automation
Site: https://the-internet.herokuapp.com/login 
Description:
    Demonstrates automated login testing using Selenium WebDriver.
    Covers valid login, invalid login error handling, and logout flow.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://the-internet.herokuapp.com/login"
VALID_USER = "tomsmith"
VALID_PASS = "SuperSecretPassword!"
INVALID_USER = "wronguser"
INVALID_PASS = "wrongpassword"


@pytest.fixture
def driver():
    """Set up Chrome WebDriver with headless option."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


class TestLoginFlow:

    def test_valid_login(self, driver):
        """TC-001: Valid credentials should redirect to secure area."""
        driver.get(BASE_URL)

        driver.find_element(By.ID, "username").send_keys(VALID_USER)
        driver.find_element(By.ID, "password").send_keys(VALID_PASS)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        success_msg = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.success"))
        )

        assert "You logged into a secure area!" in success_msg.text
        assert "/secure" in driver.current_url

    def test_invalid_username(self, driver):
        """TC-002: Invalid username should show error message."""
        driver.get(BASE_URL)

        driver.find_element(By.ID, "username").send_keys(INVALID_USER)
        driver.find_element(By.ID, "password").send_keys(VALID_PASS)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        error_msg = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )

        assert "Your username is invalid!" in error_msg.text
        assert "/login" in driver.current_url

    def test_invalid_password(self, driver):
        """TC-003: Invalid password should show error message."""
        driver.get(BASE_URL)

        driver.find_element(By.ID, "username").send_keys(VALID_USER)
        driver.find_element(By.ID, "password").send_keys(INVALID_PASS)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        error_msg = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )

        assert "Your password is invalid!" in error_msg.text

    def test_logout_after_login(self, driver):
        """TC-004: User should be able to log out after successful login."""
        driver.get(BASE_URL)

        driver.find_element(By.ID, "username").send_keys(VALID_USER)
        driver.find_element(By.ID, "password").send_keys(VALID_PASS)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("/secure"))

        logout_btn = driver.find_element(By.CSS_SELECTOR, "a[href='/logout']")
        logout_btn.click()

        wait.until(EC.url_contains("/login"))
        flash = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.success"))
        )

        assert "You logged out of the secure area!" in flash.text

    def test_empty_fields(self, driver):
        """TC-005: Submitting empty fields should show validation error."""
        driver.get(BASE_URL)

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        error_msg = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )

        assert "Your username is invalid!" in error_msg.text
