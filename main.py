from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Product import Product
import time
import csv

def start_driver():
    options = Options()
    options.headless = False
    options.add_argument("window-size=1920,1080")
    return webdriver.Chrome(options=options)

def accept_cookies(driver):
    button_accept = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))
    )
    button_accept.click()

def search_for(driver, query):
    input_area = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@data-cy='search-bar-input']"))
    )
    input_area.click()
    time.sleep(0.5)
    input_area.send_keys(query)
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//button[@name='searchBtn']").click()

def scrape_products(driver):
    products = []
    free_products = []

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    cards = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//div[@data-cy='l-card']"))
    )

    for card in cards:
        title = safe_text(card, ".//h4", "No title")
        price = safe_text(card, ".//p[@data-testid='ad-price']", "No price")
        link = safe_attr(card, ".//a", "href", "No link")

        product = Product(title, price, link)
        if "Za darmo" in price:
            free_products.append(product)
        else:
            products.append(product)

    return products, free_products

def paginate_and_scrape(driver, pages):
    all_products = []
    all_free_products = []

    page = 1
    while True:
        print(f"Scraping page {page}...")
        products, free_products = scrape_products(driver)
        all_products.extend(products)
        all_free_products.extend(free_products)

        try:
            next_button = driver.find_element(By.XPATH, "//a[@data-testid='pagination-forward']")
            next_href = next_button.get_attribute("href")
            if not next_href:
                break
            driver.get(next_href)
            time.sleep(2)

            page += 1
            if pages is not None and page >= pages: break
            
        except:
            print("No more pages.")
            break

    return all_products, all_free_products



def safe_text(card, xpath, default):
    try:
        return card.find_element(By.XPATH, xpath).text
    except:
        return default

def safe_attr(card, xpath, attr, default):
    try:
        return card.find_element(By.XPATH, xpath).get_attribute(attr)
    except:
        return default

def save_csv(filename, products):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Link"])
        for p in products:
            writer.writerow([p.title, p.price, p.link])

def main():
    driver = start_driver()
    driver.get("https://olx.pl")
    accept_cookies(driver)
    search_for(driver, "book")
    products, free_products = paginate_and_scrape(driver, 5)
    driver.quit()

    save_csv("products.csv", products)
    save_csv("free_products.csv", free_products)

    print(f"Saved {len(products)} normal products and {len(free_products)} free products.")

if __name__ == "__main__":
    main()
