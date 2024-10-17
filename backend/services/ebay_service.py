import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# eBay API credentials
EBAY_APP_ID = os.getenv('SamuelTs-Garmentz-PRD-c4f84c9e4-f2356953')
EBAY_DEV_ID = os.getenv('b7535707-f3c1-4b2f-bf43-dd4ac4b60d41')
EBAY_CERT_ID = os.getenv('SBX-4f97b41c1267-bbf8-47d5-904a-6526')
EBAY_REDIRECT_URI = os.getenv('Samuel_Tsega-SamuelTs-Garmen-usxnk')
EBAY_OAUTH_TOKEN = os.getenv('v^1.1#i^1#f^0#p^3#r^0#I^3#t^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')

# eBay API endpoint
EBAY_API_ENDPOINT = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search?q=drone&limit=3"

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

