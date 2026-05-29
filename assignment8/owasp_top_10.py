import os
import re
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://owasp.org/www-project-top-ten/"

ITEM_RE = re.compile(r"^A(0[1-9]|10)\b")


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


def scrape_owasp():
    driver = make_driver()
    try:
        driver.get(URL)
        release = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href,'/Top10/') and contains(.,'Top 10:')]")
            )
        )
        release_url = release.get_attribute("href")

        time.sleep(2)
        driver.get(release_url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/Top10/')]"))
        )

        vulns = []
        seen = set()
        for a in driver.find_elements(By.XPATH, "//a[contains(@href,'/Top10/')]"):
            title = a.text.strip()
            href = a.get_attribute("href")
            if ITEM_RE.match(title) and href not in seen:
                seen.add(href)
                vulns.append({"title": title, "href": href})
        return vulns
    finally:
        driver.quit()


def main():
    vulns = scrape_owasp()
    if len(vulns) != 10:
        raise ValueError(f"expected 10 risks, got {len(vulns)}")

    print(f"Found {len(vulns)} vulnerabilities")
    for v in vulns:
        print(v)

    pd.DataFrame(vulns).to_csv("owasp_top_10.csv", index=False)
    print("Written: owasp_top_10.csv")


if __name__ == "__main__":
    main()
