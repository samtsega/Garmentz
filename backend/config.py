import os
class Config: """Base configuration."""

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')

# Upload folder for images
UPLOAD_FOLDER = 'uploads' # Allowed file extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Currency conversion settings
DEFAULT_CURRENCY = 'USD'

# Default currency for the app
TARGET_CURRENCY = 'USD'

# Default target currency for conversion
CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')

# API key for currency conversion service
CURRENCY_API_URL = 'https://api.exchangerate-api.com/v4/latest/'

# Base URL for currency conversion # Example API keys for services (if needed)
EBAY_API_KEY = os.getenv('EBAY_API_KEY', 'your_ebay_api_key_here')
DEPOP_API_KEY = os.getenv('DEPOP_API_KEY', 'your_depop_api_key_here')
GRAILED_API_KEY = os.getenv('GRAILED_API_KEY', 'your_grailed_api_key_here')
SAKSFIFTH_API_KEY = os.getenv('SAKFIFTH_API_KEY', 'your_saksfifth_api_key_here')
SSENSE_API_KEY = os.getenv('SSENSE_API_KEY', 'your_ssense_api_key_here')
VESTIARE_API_KEY = os.getenv('VESTIARE_API_KEY', 'your_vestiare_api_key_here')
FARFETCH_API_KEY = os.getenv('FARFETCH_API_KEY', 'your_farfetch_api_key_here')
FASHIONPHILE_API_KEY = os.getenv('FASHIONPHILE_API_KEY', 'your_amazon_api_key_here')
AMAZON_API_KEY = os.getenv('AMAZON_API_KEY', 'your_amazon_api_key_here')

# Add more API keys as needed for other services # Optionally, if you have multiple configurations (e.g., Development, Production) class DevelopmentConfig(Config): DEBUG = True class ProductionConfig(Config): DEBUG = False # You could use this method to load the appropriate configuration based on the environment def get_config(): env = os.getenv('FLASK_ENV', 'development') if env == 'production': return ProductionConfig() return DevelopmentConfig()

# Base URLs for the respective APIs

AMAZON_API_URL = "https://api.amazon.com/product"
SSENSE_API_URL =
FARFETCH_API_URL =
SAKSFIFTH_API_URL =
FASHIONPHILE_API_URL =
GRAILED_API_URL =
AMAZON_API_URL = "https://api.amazon.com/product"
EBAY_API_URL = "https://api.ebay.com/findItems"
DEPOP_API_URL = "https://api.depop.com/v1/products"
VESTIAIRE_API_URL = "https://api.vestiairecollective.com/products"

# Timeout for API requests (in seconds)

REQUEST_TIMEOUT = 10

# Depreciation settings (e.g., the default rate of 20% per year)

DEPRECIATION_RATE = 0.20

# Log configuration
LOG_FILE_PATH = 'logs/app.log'
LOG_LEVEL = 'INFO'

# Flask settings (if applicable)

FLASK_DEBUG = True
FLASK_PORT = 5000

# Environment-specific configurations
ENV = 'development' # Change to 'production' when deploying