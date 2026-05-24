import time
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://durhamcounty.bibliocommons.com/v2/search?query=learning+spanish&searchType=smart"

def _safe_text(element, class_name):
    try:
        return element.find_element(By.CLASS_NAME, class_name).text.strip()
    except Exception:
        return "N/A"

def _join_authors(author_elements):
    authors = [a.text.strip() for a in author_elements if a.text.strip()]
    return "; ".join(authors) if authors else "N/A"

def get_books():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(URL)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cp-search-result-item"))
        )
        time.sleep(2)
        li_elements = driver.find_elements(By.XPATH, "//li[contains(@class,'cp-search-result-item')]")
        print(f"Found {len(li_elements)} results")
        results = []
        for item in li_elements:
            title = _safe_text(item, "title-content")
            author_els = item.find_elements(By.CLASS_NAME, "author-link")
            author = _join_authors(author_els)
            fmt = _safe_text(item, "cp-format-indicator")
            year = _safe_text(item, "cp-publish-year")
            parts = [p for p in (fmt, year) if p != "N/A"]
            format_year = " ".join(parts) if parts else "N/A"
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
