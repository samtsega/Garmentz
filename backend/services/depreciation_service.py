import os
import requests
import numpy as np
from tf_keras.models import load_model
from tf_keras.preprocessing import image
from datetime import datetime

# Load the model
MODEL_PATH = os.getenv('DEPRECIATION_MODEL_PATH', 'models/depreciation_model.h5')
model = load_model(MODEL_PATH)

BRAND_DEPRECIATION = {
    'brand_a': 0.1,
    'brand_b': 0.2,
    'brand_c': 0.15
}
FABRIC_DEPRECIATION = {
    'cotton': 0.1,
    'leather': 0.05,
    'polyester': 0.2,
    'wool': 0.07
}

def estimate_age_based_depreciation(age):
    depreciation_rate_per_year = 0.1  # Base depreciation rate per year
    return 1 - (depreciation_rate_per_year * age)

def get_original_price(product_id):
    api_url = f'https://api.ebay.com/some-endpoint/{product_id}'
    headers = {
        'Authorization': 'Bearer YOUR_API_TOKEN',
        'Content-Type': 'application/json'
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        original_price = data.get('price', 100)  # Fallback to 100 if not found
        return original_price
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def calculate_depreciation(image_path, brand=None, fabric=None, purchase_date=None, wear_tear_score=0, product_id=None):
    # 1. Predict the age of the clothing item
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Predict clothing's age using the model
    prediction = model.predict(img_array)
    estimated_age = prediction[0][0]

    # 2. Calculate depreciation based on age
    age_depreciation = estimate_age_based_depreciation(estimated_age)

    # 3. Adjust depreciation based on brand
    brand_depreciation_rate = BRAND_DEPRECIATION.get(brand.lower(), 0.1)

    # 4. Adjust depreciation based on fabric
    fabric_depreciation_rate = FABRIC_DEPRECIATION.get(fabric.lower(), 0.1)

    # 5. Adjust depreciation based on purchase date (if provided)
    if purchase_date:
        try:
            purchase_date_obj = datetime.strptime(purchase_date, '%Y-%m-%d')
            age_in_years = (datetime.now() - purchase_date_obj).days / 365
            age_depreciation = estimate_age_based_depreciation(age_in_years)
        except Exception as e:
            print(f"Error parsing purchase date: {e}")

    # Fetch original price from API
    original_price = get_original_price(product_id) if product_id else 100

    # 6. Combine depreciation factors with wear and tear adjustment
    final_depreciation_rate = age_depreciation * (1 - brand_depreciation_rate) * (1 - fabric_depreciation_rate) * (1 - wear_tear_score)
    current_value = original_price * final_depreciation_rate

    return {
        'original_price': original_price,
        'depreciation_rate': final_depreciation_rate,
        'current_value': current_value,
        'estimated_age': estimated_age,
        'wear_and_tear': wear_tear_score,
        'brand': brand,
        'fabric': fabric
    }
