"""
Web Scraping: E-commerce Product Data
Site: https://books.toscrape.com
Demonstrates scraping product listings with prices, ratings, and availability
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from scraper_utils import DataExporter, ScraperStats


BASE_URL = "https://books.toscrape.com"


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


class TestBookScraper:

    def test_scrape_book_listings(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod")))

        books = driver.find_elements(By.CLASS_NAME, "product_pod")

        scraped_books = []
        for book in books:
            title = book.find_element(By.TAG_NAME, "h3").text
            price = book.find_element(By.CLASS_NAME, "price_color").text

            rating_element = book.find_element(By.CLASS_NAME, "star-rating")
            rating = rating_element.get_attribute("class").split()[-1]

            try:
                availability = book.find_element(By.CLASS_NAME, "availability").text.strip()
            except NoSuchElementException:
                availability = "Unknown"

            scraped_books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability
            })

        assert len(scraped_books) > 0
        print(f"\nScraped {len(scraped_books)} books")

    def test_scrape_with_pagination(self, driver):
        driver.get(BASE_URL)

        stats = ScraperStats()
        all_books = []
        max_pages = 3

        while stats.pages_visited < max_pages:
            stats.record_page()

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod")))

            books = driver.find_elements(By.CLASS_NAME, "product_pod")

            for book in books:
                try:
                    title = book.find_element(By.TAG_NAME, "h3").text
                    price = book.find_element(By.CLASS_NAME, "price_color").text

                    all_books.append({
                        "title": title,
                        "price": price,
                        "page": stats.pages_visited
                    })
                    stats.record_item()

                except Exception as e:
                    stats.record_error()
                    continue

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.next > a")
                next_button.click()
            except NoSuchElementException:
                break

        summary = stats.get_summary()
        print(f"\n{summary['items_scraped']} books scraped from {summary['pages_visited']} pages")
        print(f"Duration: {summary['duration_seconds']}s | Rate: {summary['items_per_second']} items/s")

        assert len(all_books) > 10

    def test_scrape_and_export_to_csv(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod")))

        books = driver.find_elements(By.CLASS_NAME, "product_pod")

        scraped_books = []
        for book in books:
            title = book.find_element(By.TAG_NAME, "h3").text
            price = book.find_element(By.CLASS_NAME, "price_color").text
            rating_element = book.find_element(By.CLASS_NAME, "star-rating")
            rating = rating_element.get_attribute("class").split()[-1]

            scraped_books.append({
                "title": title,
                "price": price,
                "rating": rating
            })

        exporter = DataExporter()
        filename = exporter.generate_filename("books", "csv")
        exporter.to_csv(scraped_books, filename, fieldnames=["title", "price", "rating"])

        print(f"\nExported {len(scraped_books)} books to {filename}")

    def test_scrape_category_links(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        category_links = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".side_categories ul li ul li a"))
        )

        categories = []
        for link in category_links:
            category_name = link.text.strip()
            category_url = link.get_attribute("href")
            categories.append({
                "name": category_name,
                "url": category_url
            })

        assert len(categories) > 0
        print(f"\nFound {len(categories)} categories")

    def test_scrape_book_details(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        first_book = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".product_pod h3 a"))
        )
        first_book.click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product_main")))

        title = driver.find_element(By.TAG_NAME, "h1").text
        price = driver.find_element(By.CLASS_NAME, "price_color").text

        try:
            description = driver.find_element(By.CSS_SELECTOR, "#product_description + p").text
        except NoSuchElementException:
            description = "No description available"

        product_info = driver.find_elements(By.CSS_SELECTOR, ".table.table-striped tr")
        info_dict = {}
        for row in product_info:
            key = row.find_element(By.TAG_NAME, "th").text
            value = row.find_element(By.TAG_NAME, "td").text
            info_dict[key] = value

        book_details = {
            "title": title,
            "price": price,
            "description": description,
            "product_info": info_dict
        }

        assert book_details["title"]
        assert book_details["price"]
        print(f"\nScraped details for: {title}")

    def test_filter_books_by_rating(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod")))

        books = driver.find_elements(By.CLASS_NAME, "product_pod")

        high_rated_books = []
        for book in books:
            rating_element = book.find_element(By.CLASS_NAME, "star-rating")
            rating_class = rating_element.get_attribute("class")

            if "Four" in rating_class or "Five" in rating_class:
                title = book.find_element(By.TAG_NAME, "h3").text
                price = book.find_element(By.CLASS_NAME, "price_color").text

                high_rated_books.append({
                    "title": title,
                    "price": price,
                    "rating": rating_class.split()[-1]
                })

        print(f"\nFound {len(high_rated_books)} high-rated books (4-5 stars)")
        assert len(high_rated_books) > 0

    def test_extract_price_range(self, driver):
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod")))

        price_elements = driver.find_elements(By.CLASS_NAME, "price_color")

        prices = []
        for price_elem in price_elements:
            price_text = price_elem.text.replace('£', '').strip()
            try:
                price = float(price_text)
                prices.append(price)
            except ValueError:
                continue

        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)

            print(f"\nPrice Analysis:")
            print(f"  Min: £{min_price:.2f}")
            print(f"  Max: £{max_price:.2f}")
            print(f"  Avg: £{avg_price:.2f}")

            assert min_price < max_price
