"""
Test: Login & Navigation Automation
Site: https://the-internet.herokuapp.com
Tools: Playwright, Python (pytest-playwright)
Description:
    Demonstrates Playwright browser automation for login flows,
    navigation, and assertions. Uses Playwright's modern async-friendly
    API with auto-waiting built in.

Install:
    pip install pytest-playwright
    playwright install chromium
Run:
    pytest test_login_playwright.py -v
"""

import pytest
from playwright.sync_api import Page, expect


BASE_URL = "https://the-internet.herokuapp.com"


@pytest.fixture(scope="function")
def login_page(page: Page):
    """Navigate to the login page before each test."""
    page.goto(f"{BASE_URL}/login")
    return page


class TestLoginPlaywright:

    def test_successful_login(self, login_page: Page):
        """TC-001: Valid credentials should log in and show success message."""
        login_page.fill("#username", "tomsmith")
        login_page.fill("#password", "SuperSecretPassword!")
        login_page.click("button[type='submit']")

        expect(login_page.locator(".flash.success")).to_be_visible()
        expect(login_page.locator(".flash.success")).to_contain_text("You logged into a secure area!")
        assert "/secure" in login_page.url

    def test_failed_login_invalid_password(self, login_page: Page):
        """TC-002: Wrong password should display an error."""
        login_page.fill("#username", "tomsmith")
        login_page.fill("#password", "badpassword")
        login_page.click("button[type='submit']")

        expect(login_page.locator(".flash.error")).to_be_visible()
        expect(login_page.locator(".flash.error")).to_contain_text("Your password is invalid!")

    def test_failed_login_invalid_username(self, login_page: Page):
        """TC-003: Wrong username should display an error."""
        login_page.fill("#username", "baduser")
        login_page.fill("#password", "SuperSecretPassword!")
        login_page.click("button[type='submit']")

        expect(login_page.locator(".flash.error")).to_be_visible()
        expect(login_page.locator(".flash.error")).to_contain_text("Your username is invalid!")

    def test_logout_flow(self, login_page: Page):
        """TC-004: User should be able to log out after logging in."""
        login_page.fill("#username", "tomsmith")
        login_page.fill("#password", "SuperSecretPassword!")
        login_page.click("button[type='submit']")

        # Wait for secure page to load
        expect(login_page.locator("h2")).to_contain_text("Secure Area")

        # Click logout
        login_page.click("a[href='/logout']")

        expect(login_page.locator(".flash.success")).to_contain_text("You logged out")
        assert login_page.url == f"{BASE_URL}/login"

    @pytest.mark.parametrize("username,password,error_text", [
        ("tomsmith", "wrongpass", "password is invalid"),
        ("wronguser", "SuperSecretPassword!", "username is invalid"),
    ])
    def test_invalid_credentials_parametrized(self, login_page: Page, username, password, error_text):
        """TC-005: Parametrized invalid login scenarios."""
        login_page.fill("#username", username)
        login_page.fill("#password", password)
        login_page.click("button[type='submit']")

        error = login_page.locator(".flash.error")
        expect(error).to_be_visible()
        expect(error).to_contain_text(error_text)
