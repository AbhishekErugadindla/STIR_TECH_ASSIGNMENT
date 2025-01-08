# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# import chromedriver_autoinstaller


# def setup_driver():
#     chrome_options = Options()

#     # Railway-specific Chrome options
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-notifications')
#     chrome_options.add_argument('--window-size=1920,1080')
#     chrome_options.add_argument('--remote-debugging-port=9222')

#     try:
#         chromedriver_autoinstaller.install()
#         driver = webdriver.Chrome(options=chrome_options)
#         return driver
#     except Exception as e:
#         print(f"Error creating WebDriver: {str(e)}")
#         raise
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import logging

logger = logging.getLogger(__name__)

def setup_driver():
    try:
        chrome_options = Options()
        
        # Essential Chrome options for Render environment
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--remote-debugging-port=9222')
        
        # Set binary location for Chromium
        chrome_binary_location = os.getenv('CHROME_BINARY_LOCATION', '/usr/bin/chromium')
        chrome_options.binary_location = chrome_binary_location
        
        # Set up Chrome service with explicit driver path
        service = Service(executable_path='/usr/bin/chromedriver')
        
        # Create and return the driver
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        
        logger.info("WebDriver setup successful")
        return driver
        
    except Exception as e:
        logger.error(f"Error creating WebDriver: {str(e)}")
        raise
