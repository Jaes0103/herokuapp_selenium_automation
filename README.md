# 🤖 Automation Portfolio

A collection of browser and web automation scripts built with **Selenium WebDriver** and **Playwright** using Python. These samples demonstrate real-world automation patterns used in professional QA and automation engineering roles.

---

## 📁 Project Structure

```
automation-portfolio/
├── heroku_selenium/
│   ├── test_login.py                 # Login form automation & validation
│   ├── test_dynamic_elements.py      # Dynamic content, AJAX & wait strategies
│   ├── test_page_object_model.py     # Page Object Model (POM) design pattern
│   └── requirements.txt
│
├── web_scraping_selenium/
│   ├── test_web_scraping.py          # Quote scraping with pagination
│   ├── test_ecommerce_scraping.py    # E-commerce product scraping
│   ├── scraper_utils.py              # Data export utilities (JSON/CSV)
│   └── requirements.txt
│
└── heroku_playwright/
    ├── test_login_playwright.py      # Login flows with Playwright
    ├── test_advanced_playwright.py   # Iframes, tabs, alerts, screenshots
    └── requirements.txt
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Selenium WebDriver | Browser automation & testing |
| Playwright | Modern browser automation |
| Python | Scripting language |
| Pytest | Test runner & assertions |
| PyAutoGUI | Desktop GUI automation |

---

## 🚀 Getting Started

### Selenium Tests

```bash
cd heroku_selenium
pip install -r requirements.txt
pytest -v
```

### Web Scraping

```bash
cd web_scraping_selenium
pip install -r requirements.txt
pytest -v
```

### Playwright

```bash
cd heroku_playwright
pip install -r requirements.txt
playwright install chromium
pytest -v
```

---

## 📋 What's Covered

### Selenium Tests
- ✅ Login form automation (valid, invalid, empty fields)
- ✅ Explicit & implicit waits
- ✅ Dynamic element handling (AJAX, spinners, disappearing elements)
- ✅ Page Object Model (POM) design pattern
- ✅ Parametrized test cases
- ✅ Timeout exception handling

### Web Scraping
- ✅ Quote scraping with pagination
- ✅ E-commerce product data extraction
- ✅ Export data to JSON/CSV formats
- ✅ Author & tag filtering
- ✅ Price analysis & statistics
- ✅ JavaScript execution
- ✅ Error handling & recovery

### Playwright
- ✅ Login & logout flows
- ✅ Checkbox and dropdown interactions
- ✅ Hover effects
- ✅ JavaScript alert & confirm dialog handling
- ✅ Iframe content interaction
- ✅ New tab / popup handling
- ✅ Screenshot capture at key steps
- ✅ Parametrized tests