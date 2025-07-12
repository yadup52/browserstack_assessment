import time
import os
import requests
from selenium import webdriver
from translate_header import translate_and_analyze_titles
from selenium.webdriver.common.by import By

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

def scrape_articles(driver):
    driver.get("https://elpais.com")
    time.sleep(5)

    try:
        time.sleep(2)
        consent_button = driver.find_element(By.ID, "didomi-notice-agree-button")
        driver.execute_script("arguments[0].click();", consent_button)
        time.sleep(2)
        print("Cookie consent accepted.")
    except Exception as e:
        print("No cookie notice or already accepted.")

    try:
        time.sleep(3)
        opinion_link = driver.find_element(By.LINK_TEXT, "OPINIÓN")
        driver.execute_script("arguments[0].scrollIntoView(true);", opinion_link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", opinion_link)
        time.sleep(5)
        print("Navigated to OPINIÓN section.")
    except Exception as e:
        print("Failed to navigate to OPINIÓN section:", e)
        return []

    articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
    data = []

    for i, article in enumerate(articles):
        try:
            title = article.find_element(By.TAG_NAME, "h2").text.strip()

            try:
                content = article.find_element(By.TAG_NAME, "p").text.strip()
            except:
                content = "(No summary found)"

            try:
                image_url = article.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

                if image_url and image_url.startswith("http"):
                    os.makedirs("screenshots", exist_ok=True)
                    img_name = f"screenshots/{title[:15].replace(' ', '_').replace('/', '').replace(':', '')}.jpg"
                    with open(img_name, "wb") as f:
                        f.write(requests.get(image_url).content)
                    print("Image downloaded.")
                else:
                    print(" Image URL is not valid.")
            except Exception as e:
                image_url = None

            data.append({
                "title": title,
                "content": content,
                "image_url": image_url
            })

        except Exception as e:
            print(f" Error scraping article {i+1}: {e}")
            continue

    return data

def test_scraper():
    driver = setup_driver()
    try:
        articles = scrape_articles(driver)
        for i, article in enumerate(articles, 1):
            print(f"\nArticle {i}")
            print("Title:", article['title'])
            print("Content Snippet:", article['content'][:150], "...")

        translate_and_analyze_titles(articles)

    finally:
        driver.quit()
