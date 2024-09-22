from models.image_model import process_image
from routes.price_scraper import get_price_from_amazon, get_price_from_ebay


def calculate_depreciation(original_price, age):
    depreciation_rate = 0.10
# Example: 10% depreciation per year
    depreciated_value = original_price * (1 - (depreciation_rate * age))
    return max(depreciated_value, 0)

def scan_clothes(image):
    # Process image to get brand, fabric, and age
    clothing_data = process_image(image)
    brand = clothing_data['brand']
    fabric = clothing_data['fabric']
    age = clothing_data['age']

# Fetch pricing from Amazon and eBay
amazon_price = get_price_from_amazon(brand, fabric).get('price')
ebay_price = get_price_from_ebay(brand, fabric).get('price')

# Assume average of both prices
average_price = (amazon_price + ebay_price) / 2

# Apply depreciation

final_price = calculate_depreciation(average_price, age)

return {
    "brand": brand,
    "fabric": fabric,
    "age": age,
    "price": final_price
}