"""
Playwright Test: Advanced Browser Automation
Site: https://the-internet.herokuapp.com
Description:
    Demonstrates Playwright capabilities including:
    - Multi-tab / new window handling
    - File download detection
    - Network request interception
    - Screenshot capture on failure
    - Drag and drop interaction
"""

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, expect


BASE_URL = "https://the-internet.herokuapp.com"


@pytest.fixture(scope="function")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()


@pytest_asyncio.fixture
async def page(browser):
    context = await browser.new_context()
    page = await context.new_page()
    yield page


class TestAdvancedPlaywright:

    @pytest.mark.asyncio
    async def test_new_tab_handling(self, browser):
        """TC-001: Clicking a link that opens a new tab is handled correctly."""
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f"{BASE_URL}/windows")

        # Wait for new tab to open
        async with context.expect_page() as new_page_info:
            await page.click("a[href='/windows/new']")

        new_page = await new_page_info.value
        await new_page.wait_for_load_state()

        heading = new_page.locator("h3")
        await expect(heading).to_contain_text("New Window")
        await context.close()

    @pytest.mark.asyncio
    async def test_file_download(self, browser):
        """TC-002: File downloads are detected and handled correctly."""
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        await page.goto(f"{BASE_URL}/download")

        links = page.locator("a")
        count = await links.count()
        assert count > 0, "No downloadable files found on page"

        async with page.expect_download() as download_info:
            await links.first.click()

        download = await download_info.value
        assert download.suggested_filename != "", "Download filename should not be empty"
        await context.close()

    @pytest.mark.asyncio
    async def test_network_request_interception(self, browser):
        """TC-003: Network requests can be intercepted and inspected."""
        context = await browser.new_context()
        page = await context.new_page()

        intercepted_urls = []

        async def handle_request(request):
            intercepted_urls.append(request.url)

        page.on("request", handle_request)

        await page.goto(f"{BASE_URL}/login")

        assert any(BASE_URL in url for url in intercepted_urls), (
            "Expected at least one request to the base URL"
        )

        await context.close()

    @pytest.mark.asyncio
    async def test_screenshot_on_failure(self, browser):
        """TC-004: Screenshots are captured for debugging on assertion failure."""
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(f"{BASE_URL}/login")
            heading = page.locator("h2")
            await expect(heading).to_contain_text("Login Page")

        except Exception:
            await page.screenshot(path="screenshot_on_failure.png")
            raise

        finally:
            await context.close()

    @pytest.mark.asyncio
    async def test_drag_and_drop(self, browser):
        """TC-005: Drag and drop interaction works as expected."""
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f"{BASE_URL}/drag_and_drop")

        column_a = page.locator("#column-a")
        column_b = page.locator("#column-b")

        initial_a_text = await column_a.locator("header").text_content()

        await column_a.drag_to(column_b)

        new_a_text = await column_a.locator("header").text_content()

        assert new_a_text != initial_a_text, (
            "Column A header should have changed after drag and drop"
        )
        await context.close()

    @pytest.mark.asyncio
    async def test_iframe_interaction(self, browser):
        """TC-006: Elements inside iframes can be located and interacted with."""
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f"{BASE_URL}/frames/iframe")

        frame = page.frame_locator("#mce_0_ifr")
        body = frame.locator("body#tinymce")

        await body.click()
        await body.fill("Automation test input inside iframe")

        content = await body.text_content()
        assert "Automation test input inside iframe" in content
        await context.close()
