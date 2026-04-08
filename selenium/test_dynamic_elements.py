"""
Test: Dynamic Elements & Wait Strategies
Site: https://the-internet.herokuapp.com 
Description:
    Demonstrates handling of dynamic web content — disappearing elements,
    loading spinners, and AJAX-driven UI changes using explicit waits.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


class TestDynamicElements:

    def test_dynamic_loading_waits_for_content(self, driver):
        """
        TC-001: Page with a loading spinner should eventually reveal content.
        Demonstrates: Explicit wait until element is visible after AJAX load.
        """
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

        start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
        start_button.click()

        wait = WebDriverWait(driver, 15)

        # Wait for the loading spinner to disappear
        wait.until(EC.invisibility_of_element_located((By.ID, "loading")))

        # Wait for the finished text to appear
        finish_text = wait.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        assert finish_text.is_displayed()
        assert "Hello World!" in finish_text.text

    def test_disappearing_element(self, driver):
        """
        TC-002: Some elements randomly appear/disappear on page load.
        Demonstrates: Checking element presence without crashing the test.
        """
        driver.get("https://the-internet.herokuapp.com/disappearing_elements")

        nav_items = driver.find_elements(By.CSS_SELECTOR, "ul li a")
        nav_texts = [item.text for item in nav_items]

        # Home and About should always be present
        assert "Home" in nav_texts
        assert "About" in nav_texts

        # Gallery is the dynamic element — just check it without failing if absent
        print(f"Navigation items found: {nav_texts}")
        print(f"'Gallery' present: {'Gallery' in nav_texts}")

    def test_dynamic_controls_checkbox(self, driver):
        """
        TC-003: Checkbox appears/disappears via a button click with AJAX.
        Demonstrates: Waiting for element to be removed from / added to the DOM.
        """
        driver.get("https://the-internet.herokuapp.com/dynamic_controls")

        wait = WebDriverWait(driver, 15)

        # Click the Remove button to remove the checkbox
        remove_button = driver.find_element(By.CSS_SELECTOR, "button[onclick='swapCheckbox()']")
        remove_button.click()

        # Wait until checkbox is gone from DOM
        wait.until(EC.invisibility_of_element_located((By.ID, "checkbox")))

        message = wait.until(
            EC.visibility_of_element_located((By.ID, "message"))
        )
        assert "It's gone!" in message.text

        # Click Add to bring it back
        add_button = driver.find_element(By.CSS_SELECTOR, "button[onclick='swapCheckbox()']")
        add_button.click()

        wait.until(EC.visibility_of_element_located((By.ID, "checkbox")))

        message = wait.until(
            EC.text_to_be_present_in_element((By.ID, "message"), "It's back!")
        )
        assert message

    def test_explicit_wait_timeout_handling(self, driver):
        """
        TC-004: Demonstrate graceful timeout handling.
        Demonstrates: Catching TimeoutException without crashing the test suite.
        """
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

        try:
            # Try to find an element that won't appear (too short wait time)
            wait = WebDriverWait(driver, 1)
            wait.until(EC.visibility_of_element_located((By.ID, "finish")))
        except TimeoutException:
            print("Element did not appear within the timeout — handled gracefully.")
            assert True  # Test passes: timeout was handled without a crash
