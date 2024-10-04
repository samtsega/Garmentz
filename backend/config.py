import os

# Paths to models
WEAR_AND_TEAR_MODEL_PATH = os.getenv('WEAR_AND_TEAR_MODEL_PATH', 'models/wear_and_tear_model.h5')

# Currency conversion API
CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY', 'your_currency_api_key')
CURRENCY_API_URL = os.getenv('CURRENCY_API_URL', 'https://api.exchangerate-api.com/v4/latest')

# Depreciation model path
DEPRECIATION_MODEL_PATH = os.getenv('DEPRECIATION_MODEL_PATH', 'models/depreciation_model.h5')

# Other config variables
DEBUG_MODE = os.getenv('DEBUG_MODE', True)