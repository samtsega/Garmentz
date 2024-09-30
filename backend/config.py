# config.py
# API Keys

AMAZON_API_KEY = 'your_amazon_api_key'
EBAY_API_KEY = 'your_ebay_api_key'
DEPOP_API_KEY = 'your_depop_api_key'
SSENSE_API_KEY = 'your_ssense_api_key'
GRAILED_API_KEY = 'your_grailed_api_key'
FARFETCH_API_KEY = 'your_farfetch_api_key'
STOCKX_API_KEY = 'your_stockx_api_key'
SAKSFIFTH_API_KEY = 'your_saksfifth_apikey'
FASHIONPHILE_API_KEY = 'your_depop_api_key'
VESTIAIRE_API_KEY = 'your_vestiaire_api_key'


# Base URLs for the respective APIs

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