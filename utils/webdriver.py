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
from webdriver_manager.chrome import ChromeDriverManager
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
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        
        # Create the driver with default ChromeDriver path
        service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        
        logger.info("WebDriver setup successful")
        return driver
        
    except Exception as e:
        logger.error(f"Error creating WebDriver: {str(e)}")
        raise
