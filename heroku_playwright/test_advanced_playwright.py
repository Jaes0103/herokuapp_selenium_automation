"""
Test: Multi-Page Flows, Screenshots & Assertions
Site: https://the-internet.herokuapp.com
Tools: Playwright, Python (pytest-playwright)
Description:
    Demonstrates Playwright's powerful features:
    - Multi-step page navigation
    - Screenshot capture on failure
    - Form interactions (checkboxes, dropdowns, file upload)
    - Iframe handling
    - New tab / popup handling

Install:
    pip install pytest-playwright
    playwright install chromium
Run:
    pytest test_advanced_playwright.py -v
"""

import pytest
from playwright.sync_api import Page, expect
import os


BASE_URL = "https://the-internet.herokuapp.com"
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


class TestFormInteractions:

    def test_checkboxes(self, page: Page):
        """TC-001: Interact with checkboxes and verify state."""
        page.goto(f"{BASE_URL}/checkboxes")

        checkboxes = page.locator("input[type='checkbox']")
        expect(checkboxes).to_have_count(2)

        # Check the first checkbox
        first = checkboxes.nth(0)
        if not first.is_checked():
            first.check()
        expect(first).to_be_checked()

        # Uncheck the second checkbox
        second = checkboxes.nth(1)
        if second.is_checked():
            second.uncheck()
        expect(second).not_to_be_checked()

    def test_dropdown_selection(self, page: Page):
        """TC-002: Select options from a dropdown menu."""
        page.goto(f"{BASE_URL}/dropdown")

        dropdown = page.locator("#dropdown")

        # Select by visible text
        dropdown.select_option(label="Option 1")
        expect(dropdown).to_have_value("1")

        # Select by value
        dropdown.select_option(value="2")
        expect(dropdown).to_have_value("2")

    def test_hover_reveals_element(self, page: Page):
        """TC-003: Hovering over an element should reveal hidden content."""
        page.goto(f"{BASE_URL}/hovers")

        figures = page.locator(".figure")
        expect(figures).to_have_count(3)

        # Hover over the first figure
        figures.nth(0).hover()

        caption = figures.nth(0).locator(".figcaption")
        expect(caption).to_be_visible()
        expect(caption).to_contain_text("name: user1")

    def test_javascript_alert_handling(self, page: Page):
        """TC-004: Handle a JavaScript alert dialog."""
        page.goto(f"{BASE_URL}/javascript_alerts")

        # Auto-accept any dialog that appears
        page.on("dialog", lambda dialog: dialog.accept())

        page.click("button[onclick='jsAlert()']")

        result = page.locator("#result")
        expect(result).to_contain_text("You successfully clicked an alert")

    def test_javascript_confirm_dismiss(self, page: Page):
        """TC-005: Dismiss a JavaScript confirm dialog."""
        page.goto(f"{BASE_URL}/javascript_alerts")

        page.on("dialog", lambda dialog: dialog.dismiss())
        page.click("button[onclick='jsConfirm()']")

        result = page.locator("#result")
        expect(result).to_contain_text("You clicked: Cancel")


class TestIframeHandling:

    def test_interact_with_iframe_content(self, page: Page):
        """TC-006: Switch into an iframe and interact with its content."""
        page.goto(f"{BASE_URL}/iframe")

        # Locate iframe and get its content frame
        iframe = page.frame_locator("#mce_0_ifr")

        # Type into the editor inside the iframe
        editor_body = iframe.locator("body")
        editor_body.click()
        editor_body.fill("Automation test input inside an iframe")

        expect(editor_body).to_contain_text("Automation test input inside an iframe")


class TestTabAndPopupHandling:

    def test_new_tab_handling(self, page: Page):
        """TC-007: Handle links that open in a new browser tab."""
        page.goto(f"{BASE_URL}/windows")

        # Wait for the new page/tab to open
        with page.context.expect_page() as new_page_info:
            page.click("a[href='/windows/new']")

        new_page = new_page_info.value
        new_page.wait_for_load_state()

        expect(new_page.locator("h3")).to_contain_text("New Window")

        new_page.close()


class TestScreenshotCapture:

    def test_take_screenshot_on_key_step(self, page: Page):
        """TC-008: Capture a screenshot at a key step in the automation flow."""
        page.goto(f"{BASE_URL}/login")

        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")

        # Screenshot before clicking login
        page.screenshot(path=f"{SCREENSHOT_DIR}/before_login.png")

        page.click("button[type='submit']")

        expect(page.locator(".flash.success")).to_be_visible()

        # Screenshot after successful login
        page.screenshot(path=f"{SCREENSHOT_DIR}/after_login.png")

        assert os.path.exists(f"{SCREENSHOT_DIR}/before_login.png")
        assert os.path.exists(f"{SCREENSHOT_DIR}/after_login.png")
