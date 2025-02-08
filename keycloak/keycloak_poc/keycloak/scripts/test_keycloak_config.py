import os
import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Constants
KEYCLOAK_URL = "http://keycloak:8080/"
ADMIN_UI_URL = "http://keycloak:8080/admin/master/console/"
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "permanent_admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "strong_permanent_password")
REALM_NAME = "pocrealm"

def check_url_status(url):
    """Check if the URL is accessible and print the response status and body."""
    try:
        response = requests.get(url)
        logging.info(f"[URL Status] URL: {url}, Status Code: {response.status_code}")
        logging.debug(f"[URL Body] Response Body: {response.text[:500]}")  # Limit output to first 500 chars
        if response.status_code == 404:
            logging.error(f"[❌] URL Not Found: {url}")
            return False
        logging.info(f"[✅] URL Exists: {url}")
        return True
    except requests.exceptions.RequestException as e:
        logging.warning(f"[❌] Request Error: {e}")
        return False

def setup_driver():
    """Setup Selenium WebDriver with Chrome in headless mode."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    return webdriver.Chrome(options=chrome_options)

def login_to_keycloak(driver):
    """Log in to Keycloak admin panel."""
    driver.get(KEYCLOAK_URL + "admin/")
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(ADMIN_USERNAME)
        driver.find_element(By.ID, "password").send_keys(ADMIN_PASSWORD)
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        
        # Ensure login was successful
        WebDriverWait(driver, 15).until(lambda d: "admin" in d.current_url or "login" not in d.current_url)
        logging.info("[✅] Login successful")
    except Exception as e:
        logging.error(f"[❌] Login failed: {e}")
        driver.quit()
        exit(1)

def list_realms(driver):
    """Fetch and check for 'pocrealm' in the Keycloak admin UI page."""
    driver.get(ADMIN_UI_URL)
    try:
        # Wait for the page to load (waiting for the body to be present)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Capture all the HTML content of the page
        page_source = driver.page_source
        
        # Log the first 2000 characters of the HTML content for debugging
        logging.info("[📄] Full HTML content of the page:\n" + page_source[:2000])  # Limit to first 2000 chars

        # Check if 'pocrealm' is in the page source
        if "pocrealm" in page_source:
            logging.info("[✅] Realm 'pocrealm' found successfully.")
            return True  # Return True indicating successful check
        else:
            logging.error("[❌] Realm 'pocrealm' not found.")
            return False  # Return False indicating failure to find the realm

    except Exception as e:
        logging.error(f"[❌] Failed to fetch realms: {e}")
        driver.quit()
        exit(1)

def run_tests():
    """Run the Selenium tests."""
    realm_url = KEYCLOAK_URL + f"admin/master/console/#/{REALM_NAME}"
    if not check_url_status(realm_url):
        exit(1)
    
    driver = setup_driver()
    try:
        login_to_keycloak(driver)
        list_realms(driver)
        logging.info("[✅] All tests passed!")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
