"""
Utility Helpers for Automation Portfolio
Author: Jessca Belle Bagolor
Description:
    Reusable helper functions shared across Selenium and Playwright test suites.
    Includes screenshot capture, wait helpers, and element utilities.
"""

import os
import time
from datetime import datetime


def get_timestamp():
    """Return a formatted timestamp string for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_screenshot_selenium(driver, name: str, folder: str = "screenshots"):
    """
    Capture and save a screenshot using Selenium WebDriver.

    Args:
        driver: Selenium WebDriver instance
        name: Base name for the screenshot file
        folder: Directory to save screenshots (created if not exists)
    """
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{name}_{get_timestamp()}.png"
    driver.save_screenshot(filename)
    print(f"[Screenshot] Saved: {filename}")
    return filename


async def save_screenshot_playwright(page, name: str, folder: str = "screenshots"):
    """
    Capture and save a screenshot using Playwright.

    Args:
        page: Playwright page instance
        name: Base name for the screenshot file
        folder: Directory to save screenshots (created if not exists)
    """
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{name}_{get_timestamp()}.png"
    await page.screenshot(path=filename)
    print(f"[Screenshot] Saved: {filename}")
    return filename


def retry(func, retries: int = 3, delay: float = 1.0):
    """
    Retry a function call up to a specified number of times.

    Args:
        func: Callable to retry
        retries: Maximum number of attempts
        delay: Seconds to wait between attempts

    Returns:
        Result of the successful function call

    Raises:
        Last exception if all retries fail
    """
    last_exception = None
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as e:
            last_exception = e
            print(f"[Retry] Attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)
    raise last_exception


def is_element_visible_selenium(driver, by, value) -> bool:
    """
    Check if an element is visible on the page (Selenium).

    Args:
        driver: Selenium WebDriver instance
        by: Selenium By locator strategy
        value: Locator value

    Returns:
        True if element exists and is displayed, False otherwise
    """
    try:
        element = driver.find_element(by, value)
        return element.is_displayed()
    except Exception:
        return False


def format_test_result(test_name: str, passed: bool, message: str = "") -> str:
    """
    Format a test result summary line for logging.

    Args:
        test_name: Name of the test case
        passed: Whether the test passed
        message: Optional message or error detail

    Returns:
        Formatted result string
    """
    status = "✅ PASS" if passed else "❌ FAIL"
    result = f"{status} | {test_name}"
    if message:
        result += f" | {message}"
    return result
