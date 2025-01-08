
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# def setup_driver():
#     chrome_options = Options()
    
#     # Required options for running Chrome in container
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-notifications')
#     chrome_options.add_argument('--window-size=1920,1080')
#     chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#     chrome_options.add_argument('--disable-infobars')
#     chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
#     chrome_options.binary_location = "/usr/bin/google-chrome"
    
#     # Create and return the driver
#     service = Service()
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     return driver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging

logger = logging.getLogger(__name__)

def setup_driver():
    chrome_options = Options()
    
    # Required options for running Chrome in container
    chrome_options.add_argument('--headless=new')  # Updated headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-infobars')
    
    # Additional options to help avoid detection
    chrome_options.add_argument('--lang=en-US,en;q=0.9')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    # Set user agent
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Set binary location for Chrome
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    try:
        # Create and return the driver
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP commands to avoid detection
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Add additional properties to avoid detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    except Exception as e:
        logger.error(f"Error setting up WebDriver: {str(e)}")
        raise
