# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import chromedriver_autoinstaller
#
#
# def setup_driver():
#     chrome_options = Options()
#
#     # Railway-specific Chrome options
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-notifications')
#     chrome_options.add_argument('--window-size=1920,1080')
#     chrome_options.add_argument('--remote-debugging-port=9222')
#
#     try:
#         chromedriver_autoinstaller.install()
#         options = webdriver.ChromeOptions()
#         driver = webdriver.Chrome(options=options)
#         return driver
#     except Exception as e:
#         print(f"Error creating WebDriver: {str(e)}")
#         raise
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    chrome_options = Options()
    
    # Required options for running Chrome in container
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    # Create and return the driver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

        
