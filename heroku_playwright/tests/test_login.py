"""
Playwright Test: Login & Form Automation
Site: https://the-internet.herokuapp.com (public testing site)
Author: Jessca Belle Bagolor
Description:
    Demonstrates browser automation using Playwright with async support.
    Covers login flow, form interaction, and navigation validation.
"""

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, expect


BASE_URL = "https://the-internet.herokuapp.com"
VALID_USER = "tomsmith"
VALID_PASS = "SuperSecretPassword!"


@pytest.fixture(scope="function")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def page():
    """Launch Playwright browser and yield a new page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await browser.close()


class TestLoginPlaywright:

    @pytest.mark.asyncio
    async def test_valid_login(self, page):
        """TC-001: Valid credentials log in and redirect to secure area."""
        await page.goto(f"{BASE_URL}/login")

        await page.fill("#username", VALID_USER)
        await page.fill("#password", VALID_PASS)
        await page.click("button[type='submit']")

        await expect(page).to_have_url(f"{BASE_URL}/secure")

        flash = page.locator(".flash.success")
        await expect(flash).to_contain_text("You logged into a secure area!")

    @pytest.mark.asyncio
    async def test_invalid_login(self, page):
        """TC-002: Invalid credentials show an error and stay on login page."""
        await page.goto(f"{BASE_URL}/login")

        await page.fill("#username", "baduser")
        await page.fill("#password", "badpassword")
        await page.click("button[type='submit']")

        flash = page.locator(".flash.error")
        await expect(flash).to_be_visible()
        await expect(flash).to_contain_text("Your username is invalid!")
        await expect(page).to_have_url(f"{BASE_URL}/login")

    @pytest.mark.asyncio
    async def test_logout(self, page):
        """TC-003: Logged in user can successfully log out."""
        await page.goto(f"{BASE_URL}/login")
        await page.fill("#username", VALID_USER)
        await page.fill("#password", VALID_PASS)
        await page.click("button[type='submit']")
        await expect(page).to_have_url(f"{BASE_URL}/secure")

        await page.click("a[href='/logout']")
        await expect(page).to_have_url(f"{BASE_URL}/login")

        flash = page.locator(".flash.success")
        await expect(flash).to_contain_text("You logged out of the secure area!")

    @pytest.mark.asyncio
    async def test_page_title(self, page):
        """TC-004: Login page has correct title."""
        await page.goto(f"{BASE_URL}/login")
        await expect(page).to_have_title("The Internet")

    @pytest.mark.asyncio
    async def test_login_form_elements_present(self, page):
        """TC-005: Login page renders all required form elements."""
        await page.goto(f"{BASE_URL}/login")

        await expect(page.locator("#username")).to_be_visible()
        await expect(page.locator("#password")).to_be_visible()
        await expect(page.locator("button[type='submit']")).to_be_visible()
