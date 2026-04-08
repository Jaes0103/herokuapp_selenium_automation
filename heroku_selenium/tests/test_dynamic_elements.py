"""
Selenium Test: Dynamic Elements & Wait Strategies
Site: https://the-internet.herokuapp.com (public testing site)
Author: Jessca Belle Bagolor
Description:
    Demonstrates handling of dynamic web elements, explicit waits,
    dropdowns, checkboxes, and alerts — common real-world automation challenges.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://the-internet.herokuapp.com"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


class TestDynamicElements:

    def test_checkbox_toggle(self, driver):
        """TC-001: Checkboxes can be checked and unchecked."""
        driver.get(f"{BASE_URL}/checkboxes")

        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

        # Toggle all checkboxes
        for checkbox in checkboxes:
            initial_state = checkbox.is_selected()
            checkbox.click()
            assert checkbox.is_selected() != initial_state, (
                "Checkbox state should have changed after click"
            )

    def test_dropdown_selection(self, driver):
        """TC-002: Dropdown options can be selected by value and visible text."""
        driver.get(f"{BASE_URL}/dropdown")

        dropdown = Select(driver.find_element(By.ID, "dropdown"))

        dropdown.select_by_value("1")
        assert dropdown.first_selected_option.text == "Option 1"

        dropdown.select_by_visible_text("Option 2")
        assert dropdown.first_selected_option.get_attribute("value") == "2"

    def test_javascript_alert_accept(self, driver):
        """TC-003: JavaScript alerts can be detected and accepted."""
        driver.get(f"{BASE_URL}/javascript_alerts")

        driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()

        wait = WebDriverWait(driver, 5)
        alert = wait.until(EC.alert_is_present())
        assert alert.text == "I am a JS Alert"
        alert.accept()

        result = driver.find_element(By.ID, "result")
        assert "You successfully clicked an alert" in result.text

    def test_javascript_confirm_dismiss(self, driver):
        """TC-004: JavaScript confirm dialog can be dismissed."""
        driver.get(f"{BASE_URL}/javascript_alerts")

        driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()

        wait = WebDriverWait(driver, 5)
        alert = wait.until(EC.alert_is_present())
        alert.dismiss()

        result = driver.find_element(By.ID, "result")
        assert "You clicked: Cancel" in result.text

    def test_dynamic_loading_wait(self, driver):
        """TC-005: Explicit wait handles dynamically loaded content correctly."""
        driver.get(f"{BASE_URL}/dynamic_loading/1")

        driver.find_element(By.CSS_SELECTOR, "#start button").click()

        wait = WebDriverWait(driver, 15)
        finish_text = wait.until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        assert "Hello World!" in finish_text.text

    def test_hover_reveals_element(self, driver):
        """TC-006: Hovering over an element reveals hidden content."""
        from selenium.webdriver.common.action_chains import ActionChains

        driver.get(f"{BASE_URL}/hovers")

        figures = driver.find_elements(By.CSS_SELECTOR, ".figure")
        assert len(figures) > 0, "No figure elements found on page"

        actions = ActionChains(driver)
        actions.move_to_element(figures[0]).perform()

        wait = WebDriverWait(driver, 5)
        caption = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".figure:first-child .figcaption")
            )
        )
        assert caption.is_displayed()
