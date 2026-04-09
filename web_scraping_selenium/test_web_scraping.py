"""
Web Scraping with Selenium
Site: https://quotes.toscrape.com
"""

import pytest
import json
import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


BASE_URL = "https://quotes.toscrape.com"
OUTPUT_DIR = "scraped_data"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def create_output_directory():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


class TestQuoteScraper:

    def test_scrape_single_page_quotes(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))

        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        assert len(quotes) > 0

        scraped_quotes = []
        for quote in quotes:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]

            scraped_quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        assert len(scraped_quotes) == len(quotes)
        assert all(q["text"] and q["author"] for q in scraped_quotes)
        print(f"\n✓ Scraped {len(scraped_quotes)} quotes from first page")

    def test_scrape_multiple_pages_with_pagination(self, driver):
        driver.get(BASE_URL)

        all_quotes = []
        page_count = 0
        max_pages = 3

        while page_count < max_pages:
            page_count += 1

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))

            quotes = driver.find_elements(By.CLASS_NAME, "quote")

            for quote in quotes:
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text
                tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]

                all_quotes.append({
                    "text": text,
                    "author": author,
                    "tags": tags,
                    "page": page_count
                })

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
                next_button.click()
            except NoSuchElementException:
                break

        assert len(all_quotes) > 10
        print(f"\n✓ Scraped {len(all_quotes)} quotes from {page_count} pages")

    def test_scrape_author_details(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        first_author_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".quote .author + a"))
        )

        author_name = driver.find_element(By.CLASS_NAME, "author").text
        first_author_link.click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "author-title")))

        author_info = {
            "name": driver.find_element(By.CLASS_NAME, "author-title").text,
            "born_date": driver.find_element(By.CLASS_NAME, "author-born-date").text,
            "born_location": driver.find_element(By.CLASS_NAME, "author-born-location").text,
            "description": driver.find_element(By.CLASS_NAME, "author-description").text.strip()
        }

        assert author_info["name"] == author_name
        assert author_info["born_date"]
        assert author_info["description"]
        print(f"\n✓ Scraped details for author: {author_info['name']}")

    def test_scrape_quotes_by_tag(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        tag_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".tag-item a[href*='love']"))
        )
        tag_name = tag_link.text
        tag_link.click()

        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))

        quotes = driver.find_elements(By.CLASS_NAME, "quote")

        filtered_quotes = []
        for quote in quotes:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]

            filtered_quotes.append({
                "text": text,
                "author": author,
                "tags": tags
            })

            assert tag_name in tags

        assert len(filtered_quotes) > 0
        print(f"\n✓ Scraped {len(filtered_quotes)} quotes tagged with '{tag_name}'")

    def test_scrape_and_save_to_json(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))

        quotes = driver.find_elements(By.CLASS_NAME, "quote")

        scraped_data = {
            "scrape_timestamp": datetime.now().isoformat(),
            "source_url": driver.current_url,
            "total_quotes": len(quotes),
            "quotes": []
        }

        for quote in quotes:
            scraped_data["quotes"].append({
                "text": quote.find_element(By.CLASS_NAME, "text").text,
                "author": quote.find_element(By.CLASS_NAME, "author").text,
                "tags": [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
            })

        json_filename = f"{OUTPUT_DIR}/quotes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)

        assert os.path.exists(json_filename)
        print(f"\n✓ Saved {len(scraped_data['quotes'])} quotes to {json_filename}")

    def test_scrape_and_save_to_csv(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))

        quotes = driver.find_elements(By.CLASS_NAME, "quote")

        csv_filename = f"{OUTPUT_DIR}/quotes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Quote', 'Author', 'Tags'])

            for quote in quotes:
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text
                tags = ", ".join([tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")])

                writer.writerow([text, author, tags])

        assert os.path.exists(csv_filename)
        print(f"\n✓ Saved quotes to {csv_filename}")

    def test_scrape_with_error_handling(self, driver):
        driver.get(BASE_URL)

        quotes_scraped = 0
        errors_encountered = 0

        try:
            quotes = driver.find_elements(By.CLASS_NAME, "quote")

            for quote in quotes:
                try:
                    text = quote.find_element(By.CLASS_NAME, "text").text
                    author = quote.find_element(By.CLASS_NAME, "author").text

                    try:
                        tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
                    except NoSuchElementException:
                        tags = []

                    quotes_scraped += 1

                except Exception as e:
                    errors_encountered += 1
                    print(f"Error scraping quote: {str(e)}")
                    continue

        except TimeoutException:
            print("Timeout while waiting for quotes to load")

        assert quotes_scraped > 0
        print(f"\n✓ Successfully scraped {quotes_scraped} quotes with {errors_encountered} errors")

    def test_scrape_top_ten_tags(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        tag_elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tag-item a"))
        )

        top_tags = []
        for tag in tag_elements[:10]:
            tag_name = tag.text
            tag_url = tag.get_attribute("href")

            top_tags.append({
                "name": tag_name,
                "url": tag_url
            })

        assert len(top_tags) > 0
        assert all(tag["name"] and tag["url"] for tag in top_tags)
        print(f"\n✓ Scraped top {len(top_tags)} tags: {[tag['name'] for tag in top_tags]}")


class TestAdvancedScraping:

    def test_scrape_with_javascript_execution(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))

        quote_texts = driver.execute_script("""
            const quotes = document.querySelectorAll('.quote .text');
            return Array.from(quotes).map(q => q.textContent);
        """)

        assert len(quote_texts) > 0
        assert all(text.strip() for text in quote_texts)
        print(f"\n✓ Extracted {len(quote_texts)} quotes using JavaScript")

    def test_scrape_with_scroll(self, driver):
        driver.get(BASE_URL)

        initial_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        wait = WebDriverWait(driver, 2)
        try:
            wait.until(lambda d: d.execute_script("return document.body.scrollHeight") > initial_height)
        except TimeoutException:
            pass

        driver.execute_script("window.scrollTo(0, 0);")

        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        assert len(quotes) > 0
        print(f"\n✓ Successfully scrolled page and found {len(quotes)} quotes")
