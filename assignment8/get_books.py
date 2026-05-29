import os
import json
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning+spanish&searchType=smart"


def chromedriver_path():
    path = ChromeDriverManager().install()
    if os.path.basename(path) != "chromedriver":
        path = os.path.join(os.path.dirname(path), "chromedriver")
    os.chmod(path, 0o755)
    return path


def make_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(chromedriver_path()), options=options)


def text_or_na(element, by, value):
    found = element.find_elements(by, value)
    return found[0].text.strip() if found and found[0].text.strip() else "N/A"


def get_books():
    driver = make_driver()
    try:
        driver.get(URL)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//li[contains(@class,'cp-search-result-item')]")
            )
        )
        time.sleep(2)

        items = driver.find_elements(
            By.XPATH, "//li[contains(@class,'cp-search-result-item')]"
        )
        print(f"Found {len(items)} results")

        results = []
        for item in items:
            title = text_or_na(item, By.CLASS_NAME, "title-content")

            author_els = item.find_elements(By.CLASS_NAME, "author-link")
            authors = [a.text.strip() for a in author_els if a.text.strip()]
            author = "; ".join(authors) if authors else "N/A"

            fmt_blocks = item.find_elements(By.CSS_SELECTOR,
                                            "div.cp-format-info span.display-info-primary")
            format_year = fmt_blocks[0].text.strip() if fmt_blocks else "N/A"

            results.append({"Title": title, "Author": author, "Format-Year": format_year})
        return results
    finally:
        driver.quit()


if __name__ == "__main__":
    results = get_books()

    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    print(f"\nTotal results: {len(df)}")

    df.to_csv("get_books.csv", index=False)
    print("Written: get_books.csv")

    with open("get_books.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Written: get_books.json")
