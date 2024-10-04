import os
import requests
from dotenv import load_dotenv
from botocore.signers import RequestSigner
from datetime import datetime

# Load environment variables
load_dotenv()

# Get Amazon API credentials from environment variables
ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
SECRET_KEY = os.getenv('AMAZON_SECRET_KEY')
ASSOCIATE_TAG = os.getenv('AMAZON_ASSOCIATE_TAG')
REGION = os.getenv('AMAZON_REGION', 'us-east-1')  # Default region

# Amazon PA-API endpoints
ENDPOINT = 'webservices.amazon.com'


def fetch_amazon_data(keywords):
    """
    Fetches products from Amazon based on the provided keywords.
    This function can be used in the recommendation_service.py file.
    """
    return search_product(keywords)


def sign_request(payload):
    """
    Signs the request using AWS credentials.
    """
    signer = RequestSigner(
        'execute-api',
        REGION,
        'productadvertisingapi',
        {'access_key': ACCESS_KEY, 'secret_key': SECRET_KEY, 'region_name': REGION}
    )
    headers = signer.sign('POST', ENDPOINT, '/', datetime.utcnow(), payload)
    return headers


def search_product(keywords):
    """
    Searches for products on Amazon using the given keywords.
    """
    payload = {
        'Keywords': keywords,
        'SearchIndex': 'All',
        'Resources': ['Images.Primary.Small', 'ItemInfo.Title', 'Offers.Listings.Price'],
        'PartnerTag': ASSOCIATE_TAG,
        'PartnerType': 'Associates',
    }

    headers = sign_request(payload)
    response = requests.post(f'https://{ENDPOINT}/paapi5/searchitems', json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return the search results
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def get_product_price(asin):
    """
    Fetches the product details (price, name, etc.) for the given ASIN (Amazon Standard Identification Number).
    """
    payload = {
        'ItemIds': [asin],
        'Resources': ['ItemInfo.Title', 'Offers.Listings.Price'],
        'PartnerTag': ASSOCIATE_TAG,
        'PartnerType': 'Associates',
    }

    headers = sign_request(payload)
    response = requests.post(f'https://{ENDPOINT}/paapi5/getitems', json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return product details
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


# Example Usage
if __name__ == "__main__":
    # Fetch products based on keywords
    amazon_data = fetch_amazon_data('Nike T-Shirt')
    if amazon_data:
        print(amazon_data)

    # Fetch specific product price using ASIN
    asin = 'B08L5LJSG3'  # Example ASIN
    price_data = get_product_price(asin)
    if price_data:
        print(price_data)

