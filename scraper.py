from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import pymongo
import uuid
import urllib.parse
import time
import requests
import os
from dotenv import load_dotenv
from config import Config
from utils.webdriver import setup_driver
from typing import Optional, Dict, List, Tuple
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TwitterScraper:
    def __init__(self):
        self.driver = None
        self.client = self.get_mongodb_connection()
        self.db = self.client["twitter_trends"]
        self.collection = self.db["trends"]
        self.current_ip = None
        self.proxy_mesh_url = os.getenv('PROXY_MESH_URL')
        if not self.proxy_mesh_url:
            logger.warning("PROXY_MESH_URL not found in environment variables")

    @staticmethod
    def get_mongodb_connection() -> pymongo.MongoClient:
        username = urllib.parse.quote_plus(Config.MONGODB_USERNAME)
        password = urllib.parse.quote_plus(Config.MONGODB_PASSWORD)
        connection_string = f"mongodb+srv://{username}:{password}@cluster0.40ezr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        return pymongo.MongoClient(connection_string)

    def get_current_ip(self) -> str:
        """Get current IP address using an IP checking service"""
        try:
            response = requests.get('https://api.ipify.org?format=json')
            if response.status_code == 200:
                self.current_ip = response.json()['ip']
                logger.info(f"Current IP: {self.current_ip}")
                return self.current_ip
            else:
                raise Exception("Failed to get IP address")
        except Exception as e:
            logger.error(f"Error getting IP address: {str(e)}")
            return "unknown"

    def setup_proxy(self) -> Dict[str, str]:
        """Configure ProxyMesh proxy settings from environment variables"""
        try:
            if not self.proxy_mesh_url:
                logger.error("PROXY_MESH_URL environment variable not set")
                return {}

            proxy_auth = urllib.parse.urlparse(self.proxy_mesh_url)
            proxy = {
                'http': f'http://{proxy_auth.username}:{proxy_auth.password}@{proxy_auth.hostname}:{proxy_auth.port}',
                'https': f'https://{proxy_auth.username}:{proxy_auth.password}@{proxy_auth.hostname}:{proxy_auth.port}'
            }
            logger.info("Proxy configuration successful")
            return proxy
        except Exception as e:
            logger.error(f"Error setting up proxy: {str(e)}")
            return {}

    def setup_driver(self) -> None:
        """Setup WebDriver with proxy configuration"""
        try:
            logger.info("Setting up WebDriver with proxy...")
            proxy = self.setup_proxy()
            self.driver = setup_driver()
            logger.info("WebDriver setup successful")
        except Exception as e:
            logger.error(f"Error setting up driver: {str(e)}")
            raise

    # def wait_and_find_element(self, by: By, value: str, timeout: int = 10) -> Optional[WebElement]:
    #     try:
    #         element = WebDriverWait(self.driver, timeout).until(
    #             EC.presence_of_element_located((by, value))
    #         )
    #         return element
    #     except Exception as e:
    #         logger.error(f"Error finding element {value}: {str(e)}")
    #         return None

    # def login_to_twitter(self) -> bool:
    #     """Enhanced Twitter login process with better error handling and waits"""
    #     try:
    #         logger.info("Attempting to login to Twitter...")
    #         self.driver.get("https://twitter.com/i/flow/login")
            
    #         # Wait for page load and initial rendering
    #         time.sleep(5)
            
    #         # Multiple selectors for username input
    #         username_selectors = [
    #             "//input[@autocomplete='username']",
    #             "//input[@name='text']",
    #             "//input[@autocomplete='username'][@name='text']",
    #             "//input[@type='text'][@autocomplete='username']"
    #         ]
            
    #         username_input = None
    #         for selector in username_selectors:
    #             try:
    #                 username_input = WebDriverWait(self.driver, 15).until(
    #                     EC.presence_of_element_located((By.XPATH, selector))
    #                 )
    #                 if username_input:
    #                     break
    #             except:
    #                 continue
            
    #         if not username_input:
    #             raise Exception("Could not find username input after trying multiple selectors")
            
    #         # Clear any existing text and enter username
    #         username_input.clear()
    #         for char in Config.TWITTER_USERNAME:
    #             username_input.send_keys(char)
    #             time.sleep(0.1)  # Humanize typing
            
    #         time.sleep(1)
            
    #         # Find and click the "Next" button
    #         next_button = WebDriverWait(self.driver, 15).until(
    #             EC.element_to_be_clickable((By.XPATH, "//div[@role='button']//span[text()='Next']"))
    #         )
    #         next_button.click()
            
    #         # Wait for password field with multiple possible selectors
    #         password_selectors = [
    #             "//input[@name='password']",
    #             "//input[@type='password']",
    #             "//input[@autocomplete='current-password']"
    #         ]
            
    #         password_input = None
    #         for selector in password_selectors:
    #             try:
    #                 password_input = WebDriverWait(self.driver, 5).until(
    #                     EC.presence_of_element_located((By.XPATH, selector))
    #                 )
    #                 if password_input:
    #                     break
    #             except:
    #                 continue
            
    #         if not password_input:
    #             raise Exception("Could not find password input after trying multiple selectors")
            
    #         # Clear any existing text and enter password
    #         password_input.clear()
    #         for char in Config.TWITTER_PASSWORD:
    #             password_input.send_keys(char)
    #             time.sleep(0.1)  # Humanize typing
            
    #         time.sleep(1)
            
    #         # Find and click the login button
    #         login_button = WebDriverWait(self.driver, 5).until(
    #             EC.element_to_be_clickable((By.XPATH, "//div[@role='button']//span[text()='Log in']"))
    #         )
    #         login_button.click()
            
    #         # Wait for login completion
    #         time.sleep(8)
            
    #         # Verify login success
    #         try:
    #             WebDriverWait(self.driver, 10).until(
    #                 EC.presence_of_element_located((By.XPATH, "//div[@data-testid='primaryColumn']"))
    #             )
    #             logger.info("Login successful")
    #             return True
    #         except:
    #             logger.error("Could not verify login success")
    #             return False

    #     except Exception as e:
    #         logger.error(f"Login failed: {str(e)}")
    #         # Take screenshot on failure
    #         try:
    #             screenshot_path = f"login_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    #             self.driver.save_screenshot(screenshot_path)
    #             logger.info(f"Error screenshot saved to {screenshot_path}")
    #         except:
    #             pass
    #         return False

    def wait_and_find_element(self, by: By, value: str, timeout: int = 10) -> Optional[WebElement]:
        """Enhanced element finding with multiple selectors and better error handling"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            # Ensure element is both present and visible
            if not element.is_displayed():
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
            return element
        except TimeoutException:
            logger.error(f"Timeout waiting for element: {value}")
            return None
        except Exception as e:
            logger.error(f"Error finding element {value}: {str(e)}")
            return None

    def find_username_input(self) -> Optional[WebElement]:
        """Try multiple selectors to find the username input"""
        selectors = [
            (By.XPATH, "//input[@autocomplete='username']"),
            (By.XPATH, "//input[@name='text']"),
            (By.XPATH, "//input[@type='text']"),
            (By.CSS_SELECTOR, "input[name='text']"),
            (By.CSS_SELECTOR, "input[autocomplete='username']")
        ]
        
        for by, value in selectors:
            element = self.wait_and_find_element(by, value)
            if element:
                return element
        return None

    def find_password_input(self) -> Optional[WebElement]:
        """Try multiple selectors to find the password input"""
        selectors = [
            (By.XPATH, "//input[@name='password']"),
            (By.XPATH, "//input[@type='password']"),
            (By.CSS_SELECTOR, "input[name='password']"),
            (By.CSS_SELECTOR, "input[type='password']")
        ]
        
        for by, value in selectors:
            element = self.wait_and_find_element(by, value)
            if element:
                return element
        return None

    def login_to_twitter(self) -> bool:
        """Enhanced Twitter login process with better error handling"""
        try:
            logger.info("Attempting to login to Twitter...")
            self.driver.get("https://twitter.com/i/flow/login")
            time.sleep(5)  # Allow page to fully load

            # Clear cookies and local storage
            self.driver.delete_all_cookies()
            self.driver.execute_script("window.localStorage.clear();")
            
            # Refresh page after clearing
            self.driver.refresh()
            time.sleep(3)

            # Find username input with multiple attempts
            logger.info("Looking for username input...")
            username_input = self.find_username_input()
            if not username_input:
                raise Exception("Could not find username input after multiple attempts")

            # Input username with delay between keystrokes
            for char in Config.TWITTER_USERNAME:
                username_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)
            username_input.send_keys(Keys.RETURN)
            logger.info("Username entered successfully")
            time.sleep(3)

            # Find password input
            logger.info("Looking for password input...")
            password_input = self.find_password_input()
            if not password_input:
                raise Exception("Could not find password input")

            # Input password with delay between keystrokes
            for char in Config.TWITTER_PASSWORD:
                password_input.send_keys(char)
                time.sleep(0.1)
            time.sleep(1)
            password_input.send_keys(Keys.RETURN)
            logger.info("Password entered successfully")

            # Wait for login to complete
            time.sleep(8)

            # Verify login success
            if "login" in self.driver.current_url.lower():
                raise Exception("Still on login page after attempt")

            logger.info("Login successful")
            return True

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            # Take screenshot on failure
            if self.driver:
                screenshot_path = f"login_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"Login error screenshot saved to {screenshot_path}")
            return False

 
    def get_trending_topics(self) -> List[str]:
        """Scrape trending topics from Twitter"""
        try:
            logger.info("Waiting for trends to load...")
            time.sleep(5)

            logger.info("Looking for trends element...")
            trends_section = self.wait_and_find_element(
                By.XPATH,
                "//div[@data-testid='trend']"
            )

            if not trends_section:
                logger.info("Trying alternative trend locator...")
                trends = self.driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'trend-item')]//span"
                )[:5]
            else:
                trends = self.driver.find_elements(
                    By.XPATH,
                    "//div[@data-testid='trend']//span"
                )[:5]

            trend_names = [trend.text for trend in trends if trend.text]
            logger.info(f"Found {len(trend_names)} trends")

            if len(trend_names) < 5:
                raise Exception(f"Only found {len(trend_names)} trends, need 5")

            return trend_names

        except Exception as e:
            logger.error(f"Error getting trends: {str(e)}")
            raise


            
    def save_to_mongodb(self, trends: List[str]) -> Dict[str, str]:
        """Save trending topics to MongoDB"""
        data = {
            "_id": str(uuid.uuid4()),
            "trend1": trends[0],
            "trend2": trends[1],
            "trend3": trends[2],
            "trend4": trends[3],
            "trend5": trends[4],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": self.current_ip or self.get_current_ip()
        }

        try:
            logger.info("Saving trends to MongoDB...")
            self.collection.insert_one(data)
            logger.info("Successfully saved trends to MongoDB")
            return data
        except Exception as e:
            logger.error(f"Error saving to MongoDB: {str(e)}")
            raise

    def scrape(self) -> Optional[Dict[str, str]]:
        """Main scraping method"""
        try:
            # Get current IP before starting the scraping process
            self.get_current_ip()
            self.setup_driver()

            if not self.login_to_twitter():
                raise Exception("Failed to login to Twitter")

            trends = self.get_trending_topics()
            return self.save_to_mongodb(trends)

        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            if self.driver:
                screenshot_path = f"error_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"Error screenshot saved to {screenshot_path}")
            return None

        finally:
            if self.driver:
                logger.info("Closing WebDriver...")
                self.driver.quit()



def scrape_twitter() -> Optional[Dict[str, str]]:
    """Main function to be called from Flask app"""
    scraper = TwitterScraper()
    return scraper.scrape()

