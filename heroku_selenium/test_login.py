"""
Test: Login Form Automation
Site: https://the-internet.herokuapp.com/login (public demo site)
Tools: Selenium WebDriver, Python
Author: Jessca Belle Bagolor
Description:
    Demonstrates browser automation for login form validation.
    Covers successful login, failed login, and logout flows.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


BASE_URL = "https://the-internet.herokuapp.com/login"


@pytest.fixture
def driver():
    """Set up and tear down ChromeDriver."""
    options = Options()
    options.add_argument("--headless")        # Run without opening a browser window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


class TestLogin:

    def test_successful_login(self, driver):
        """TC-001: Valid credentials should redirect to secure area."""
        driver.get(BASE_URL)

        driver.find_element(By.ID, "username").send_keys("tomsmith")
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        success_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.success"))
        )

        assert "You logged into a secure area!" in success_message.text
        assert "/secure" in driver.current_url

    def test_failed_login_wrong_password(self, driver):
        """TC-002: Invalid password should show an error message."""
        driver.get(BASE_URL)

        driver.find_element(By.ID, "username").send_keys("tomsmith")
        driver.find_element(By.ID, "password").send_keys("wrongpassword")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )

        assert "Your password is invalid!" in error_message.text

    def test_failed_login_wrong_username(self, driver):
        """TC-003: Invalid username should show an error message."""
        driver.get(BASE_URL)

        driver.find_element(By.ID, "username").send_keys("invaliduser")
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )

        assert "Your username is invalid!" in error_message.text

    def test_logout_after_login(self, driver):
        """TC-004: User should be able to log out after a successful login."""
        driver.get(BASE_URL)

        driver.find_element(By.ID, "username").send_keys("tomsmith")
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        logout_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/logout']"))
        )
        logout_button.click()

        logged_out_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.success"))
        )

        assert "You logged out of the secure area!" in logged_out_message.text
        assert driver.current_url == BASE_URL

    def test_empty_fields_submission(self, driver):
        """TC-005: Submitting empty fields should show a validation error."""
        driver.get(BASE_URL)

        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait = WebDriverWait(driver, 10)
        error_message = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )

        assert error_message.is_displayed()
