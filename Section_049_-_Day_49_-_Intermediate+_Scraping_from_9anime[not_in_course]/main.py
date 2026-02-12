from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs
import json
import time
import random

BASE_URL = "https://9animetv.to"

def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    wait = WebDriverWait(driver, 20)

    def human_delay():
        time.sleep(random.uniform(1.8, 3.5))

    def handle_popups():
        try:
            if len(driver.window_handles) > 1:
                main_window = driver.window_handles[0]
                for handle in driver.window_handles:
                    if handle != main_window:
                        driver.switch_to.window(handle)
                        driver.close()
                driver.switch_to.window(main_window)
        except:
            pass
        try:
            close_buttons = driver.find_elements(By.CSS_SELECTOR, ".close, .btn-close, .modal-close")
            for btn in close_buttons:
                try:
                    btn.click()
                except:
                    continue
        except:
            pass

    driver.get(BASE_URL)
    human_delay()
    handle_popups()

    all_link_element = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="/az-list"]')
        )
    )
    all_link_element.click()

    human_delay()
    handle_popups()

    def get_images():
        paginated_data = {}
        visited_titles = set()

        while True:
            wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.anime-block-ul > ul > li")
                )
            )

            handle_popups()
            human_delay()

            current_url = driver.current_url
            parsed = urlparse(current_url)
            page_number = parse_qs(parsed.query).get("page", ["1"])[0]
            page_key = f"page-{page_number}"

            if page_key not in paginated_data:
                paginated_data[page_key] = []

            anime_items = driver.find_elements(
                By.CSS_SELECTOR,
                "div.anime-block-ul > ul > li"
            )

            for item in anime_items:
                try:
                    title_element = item.find_element(
                        By.CSS_SELECTOR,
                        "h3.film-name > a"
                    )

                    title_text = title_element.text.strip()
                    anime_link = title_element.get_attribute("href")

                    image_element = item.find_element(
                        By.CSS_SELECTOR,
                        "img.film-poster-img"
                    )

                    image_src = image_element.get_attribute("src")
                    if not image_src:
                        image_src = image_element.get_attribute("data-src")

                    if title_text not in visited_titles:
                        visited_titles.add(title_text)
                        paginated_data[page_key].append({
                            "title": title_text,
                            "image": image_src,
                            "link": anime_link
                        })

                except:
                    continue

            try:
                next_button = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.ap__-btn-next > a:not(.disabled)"
                )

                next_page_url = next_button.get_attribute("href")
                driver.get(next_page_url)

                human_delay()
                handle_popups()

                wait.until(EC.url_contains("page="))

            except:
                break

        with open("anime_data_paginated.json", "w", encoding="utf-8") as f:
            json.dump(paginated_data, f, indent=4, ensure_ascii=False)

    get_images()
    driver.quit()

if __name__ == "__main__":
    main()
