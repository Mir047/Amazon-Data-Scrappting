import time
import re
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime

DB_NAME = "sentiment.sqlite"
TERMS_FILE = "terms.txt"
MAX_PAGES = 3
MANUAL_WAIT = 30


def read_terms(filename):
    urls = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
    return urls


def extract_asin(url):
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    return match.group(1) if match else None


def clean_review_date(raw_date):
    """
    Converts:
    'Reviewed in the United States on September 26, 2025'
    to:
    '2025-09-26'
    """
    if not raw_date:
        return None

    match = re.search(r"on (.+)", raw_date)
    if not match:
        return raw_date

    try:
        dt = datetime.strptime(match.group(1), "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return raw_date


def wait_for_manual_login(driver):
    print("Amazon login or CAPTCHA may be required.")
    print(f"Waiting {MANUAL_WAIT} seconds for manual login.")
    time.sleep(MANUAL_WAIT)
    print("Manual login wait finished.")


def scrape_reviews(driver, asin, product_name, cursor):
    page = 1
    review_url = f"https://www.amazon.com/product-reviews/{asin}"

    while review_url and page <= MAX_PAGES:
        print(f"Loading page {page} for ASIN {asin}")
        driver.get(review_url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        reviews = soup.find_all("li", {"data-hook": "review"})
        print(f"Page {page} reviews found: {len(reviews)}")

        for r in reviews:
            user = r.select_one(".a-profile-name")
            date_tag = r.select_one("span[data-hook='review-date']")
            body = r.select_one("span[data-hook='review-body']")

            message = body.get_text(strip=True) if body else ""
            if not message:
                continue

            clean_date = clean_review_date(
                date_tag.get_text(strip=True) if date_tag else None
            )

            cursor.execute("""
                INSERT INTO AMAZON_REVIEWS (Product, User, Date, Message, Sentiment)
                VALUES (?, ?, ?, ?, ?)
            """, (
                product_name,
                user.get_text(strip=True) if user else "unknown",
                clean_date,
                message,
                None
            ))

        next_btn = soup.select_one("li.a-last a")
        review_url = "https://www.amazon.com" + next_btn["href"] if next_btn else None
        page += 1


def main():
    print("Main function started")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AMAZON_REVIEWS (
            SID INTEGER PRIMARY KEY,
            Product TEXT,
            User TEXT,
            Date TEXT,
            Message TEXT,
            Sentiment TEXT
        )
    """)
    conn.commit()
    print("AMAZON_REVIEWS table ready")

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument("user-agent=Mozilla/5.0")

    print("Starting Chrome driver")
    driver = webdriver.Chrome(options=options)

    product_urls = read_terms(TERMS_FILE)
    print(f"Number of URLs found: {len(product_urls)}")

    first_time = True

    for url in product_urls:
        print(f"Processing URL: {url}")
        asin = extract_asin(url)
        if not asin:
            print("Invalid product URL, skipping")
            continue

        driver.get(url)
        time.sleep(5)

        if first_time:
            wait_for_manual_login(driver)
            first_time = False

        product_name = driver.title
        print(f"Product name: {product_name}")

        scrape_reviews(driver, asin, product_name, cursor)
        conn.commit()
        print(f"Reviews committed for: {product_name}")

    driver.quit()
    conn.close()
    print("Task 2 scraping completed successfully")


if __name__ == "__main__":
    main()

