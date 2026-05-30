from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

URL = "https://owasp.org/www-project-top-ten/"

OWASP_2021 = [
    {"title": "A01 Broken Access Control",          "href": "https://owasp.org/Top10/A01_2021-Broken_Access_Control/"},
    {"title": "A02 Cryptographic Failures",          "href": "https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"},
    {"title": "A03 Injection",                       "href": "https://owasp.org/Top10/A03_2021-Injection/"},
    {"title": "A04 Insecure Design",                 "href": "https://owasp.org/Top10/A04_2021-Insecure_Design/"},
    {"title": "A05 Security Misconfiguration",       "href": "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"},
    {"title": "A06 Vulnerable and Outdated Components", "href": "https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/"},
    {"title": "A07 Identification and Authentication Failures", "href": "https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/"},
    {"title": "A08 Software and Data Integrity Failures", "href": "https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/"},
    {"title": "A09 Security Logging and Monitoring Failures", "href": "https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/"},
    {"title": "A10 Server-Side Request Forgery",     "href": "https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_(SSRF)/"},
]

def make_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(options=options)

def scrape_owasp():
    driver = make_driver()
    driver.get(URL)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'card')]//h3"))
        )
        items = driver.find_elements(By.XPATH, "//div[contains(@class,'card')]")
        vulns = []
        for item in items:
            try:
                title = item.find_element(By.XPATH, ".//h3").text.strip()
                try:
                    href = item.find_element(By.XPATH, ".//a").get_attribute("href")
                except Exception:
                    href = ""
                if title:
                    vulns.append({"title": title, "href": href})
            except Exception:
                continue
    finally:
        driver.quit()
    if vulns:
        return vulns
    driver2 = make_driver()
    driver2.get(URL)
    try:
        WebDriverWait(driver2, 15).until(
            EC.presence_of_element_located((By.XPATH, "//li/a[contains(@href,'Top_10')]"))
        )
        links = driver2.find_elements(By.XPATH, "//li/a[contains(@href,'Top_10')]")
        vulns = [{"title": a.text.strip(), "href": a.get_attribute("href")}
                 for a in links if a.text.strip()]
    finally:
        driver2.quit()
    return vulns

def main():
    try:
        vulns = scrape_owasp()
        if not vulns:
            raise ValueError("scraper returned empty list")
    except Exception as e:
        print(f"Live scrape unavailable ({e}), using OWASP 2021 data.")
        vulns = OWASP_2021

    print(f"Found {len(vulns)} vulnerabilities")
    for v in vulns:
        print(v)

    df = pd.DataFrame(vulns)
    df.to_csv("owasp_top_10.csv", index=False)
    print("Written: owasp_top_10.csv")

if __name__ == "__main__":
    main()
