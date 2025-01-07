import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
    TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
    CHROME_BINARY_LOCATION = os.getenv('GOOGLE_CHROME_BIN', None)
    PROXY_USERNAME = os.getenv('PROXY_USERNAME')
    PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
    USE_PROXY = os.getenv('USE_PROXY', 'True').lower() == 'true'