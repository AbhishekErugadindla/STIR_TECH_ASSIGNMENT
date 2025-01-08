from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller


def setup_driver():
    chrome_options = Options()

    # Railway-specific Chrome options
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--remote-debugging-port=9222')

    try:
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Error creating WebDriver: {str(e)}")
        raise
