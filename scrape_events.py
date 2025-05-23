import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app import Event, db, app
from urllib.parse import urljoin
import logging
import time


logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_events():
    url = "https://www.eventbrite.com.au/d/australia--sydney/events/"
   
    options = webdriver.ChromeOptions()
    # Comment out headless for testing anti-bot issues
    # options.add_argument('--headless')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled') 
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = None
    soup = None

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        logging.info("WebDriver initialized successfully")
        print("WebDriver initialized successfully")

        
        try:
            driver.get(url)
            logging.info(f"Successfully loaded {url}")
            print(f"Successfully loaded {url}")
            time.sleep(3)  
        except Exception as e:
            logging.error(f"Failed to load {url}: {e}")
            print(f"Failed to load {url}: {e}")
            with open('error_page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            return

       
        max_scrolls = 5
        scroll_count = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        while scroll_count < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3) 
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_count += 1
            logging.info(f"Scrolled {scroll_count} times")
            print(f"Scrolled {scroll_count} times")

        
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.event-card'))
            )
            logging.info("Event cards loaded successfully")
            print("Event cards loaded successfully")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
        except Exception as e:
            logging.error(f"Failed to find event cards: {e}")
            print(f"Failed to find event cards: {e}")
            with open('error_page.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            return

    except Exception as e:
        logging.error(f"Failed to fetch URL with Selenium: {e}")
        print(f"Failed to fetch URL with Selenium: {e}")
        return
    finally:
        if driver:
            driver.quit()
            logging.info("WebDriver closed")
            print("WebDriver closed")

    if not soup:
        logging.error("No page source to parse")
        print("No page source to parse")
        return

    
    with open('page.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    events = []
    seen_urls = set()
    event_elements = soup.select('.event-card')
    logging.info(f"Found {len(event_elements)} event elements with selector: .event-card")
    print(f"Found {len(event_elements)} event elements with selector: .event-card")

    for event_div in event_elements:
        try:
            name_elem = event_div.select_one('[class*="title"], h3, h2')
            name = name_elem.text.strip()[:80] if name_elem else "Untitled Event"
            
            date_elem = event_div.select_one('[class*="date"], [class*="time"], p, div')
            date = date_elem.text.strip()[:120] if date_elem else "No date available"
            
            desc_elem = event_div.select_one('[class*="description"], [class*="summary"], p')
            description = desc_elem.text.strip()[:200] if desc_elem else "No description available"
            
            url_elem = event_div.select_one('a[href], [class*="cta"], [class*="link"]')
            event_url = urljoin(url, url_elem['href'])[:200] if url_elem and url_elem.get('href') else url
            
            if "Sydney" not in name and "Sydney" not in description:
                logging.info(f"Skipping non-Sydney event: {name}")
                continue

            if event_url in seen_urls:
                logging.info(f"Skipping duplicate event: {name}")
                continue
            seen_urls.add(event_url)

            events.append(Event(name=name, date=date, description=description, url=event_url))
            logging.info(f"Scraped event: {name}")
            print(f"Scraped event: {name}")
        except AttributeError as e:
            logging.warning(f"Error parsing event: {e}")
            print(f"Error parsing event: {e}")
            continue

    with app.app_context():
        try:
            Event.query.delete()
            db.session.commit()
            db.session.bulk_save_objects(events)
            db.session.commit()
            logging.info(f"Successfully saved {len(events)} events to the database.")
            print(f"Successfully saved {len(events)} events to the database.")
        except Exception as e:
            logging.error(f"Database error: {e}")
            print(f"Database error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    scrape_events()