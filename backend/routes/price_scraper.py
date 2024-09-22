import requests

# Use Amazon Product Advertising API def get_price_from_amazon(brand, fabric):
url = f"https://amazon_product_api"
params = {"brand": brand, "fabric": fabric}
response = requests.get(url, params=params)
return response.json()

# Use eBay API def get_price_from_ebay(brand, fabric):
url = f"https://ebay_api_url"
params = {"brand": brand, "fabric": fabric}
response = requests.get(url, params=params)
return response.json()
#
# Similarly, you would implement Depop and Vestiaire APIs

