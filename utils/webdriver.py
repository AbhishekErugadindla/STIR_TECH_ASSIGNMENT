
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
from webdriver_manager.chrome import ChromeDriverManager
import random
import logging

logger = logging.getLogger(__name__)

def setup_driver():
    chrome_options = Options()
    
    # Enhanced stealth settings
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-blink-features')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--lang=en-US,en')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    
    # Additional stealth settings
    chrome_options.add_argument('--disable-automation')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Random user agent with more modern versions
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    ]
    selected_agent = random.choice(user_agents)
    chrome_options.add_argument(f'user-agent={selected_agent}')
    
    # Experimental options
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Set binary location for Chrome
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    try:
        # Create and return the driver
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute CDP commands for additional stealth
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": selected_agent})
        
        # Additional stealth scripts
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
        driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['en-US', 'en']}})")
        
        logger.info("WebDriver setup successful with enhanced stealth settings")
        return driver
        
    except Exception as e:
        logger.error(f"Error setting up WebDriver: {str(e)}")
        raise
