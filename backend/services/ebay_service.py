import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# eBay API credentials
EBAY_APP_ID = os.getenv('EBAY_APP_ID')
EBAY_DEV_ID = os.getenv('EBAY_DEV_ID')
EBAY_CERT_ID = os.getenv('EBAY_CERT_ID')
EBAY_REDIRECT_URI = os.getenv('EBAY_REDIRECT_URI')
EBAY_OAUTH_TOKEN = os.getenv('EBAY_OAUTH_TOKEN')

# eBay API endpoint
EBAY_API_ENDPOINT = "https://api.ebay.com"

def fetch_ebay_data(keywords):
    """
    Fetches items from eBay based on the provided keywords.
    This function can be used in the recommendation_service.py file.
    """
    return search_items(keywords)

def search_items(keywords):
    """
    Searches for items on eBay using the given keywords.
    """
    url = f"{EBAY_API_ENDPOINT}/buy/browse/v1/search"
    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "Content-Type": "application/json",
    }
    params = {
        "q": keywords,
        "limit": 5,  # Number of items to return
        "offset": 0,
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()  # Return the search results
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_item_details(item_id):
    """
    Fetches the details of a specific item using its item ID.
    """
    url = f"{EBAY_API_ENDPOINT}/buy/browse/v1/item/{item_id}"
    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return item details
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example Usage
if __name__ == "__main__":
    # Search for items
    items_data = fetch_ebay_data('Nike Shoes')
    if items_data:
        print(items_data)

