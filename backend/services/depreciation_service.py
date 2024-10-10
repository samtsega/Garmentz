import os
import numpy as np
from tf_keras.models import load_model
from tf_keras.preprocessing import image
from datetime import datetime

# Load your trained depreciation TensorFlow model (if required)
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
    depreciation_rate_per_year = 0.1 # Base depreciation rate per year
    return 1 - (depreciation_rate_per_year * age)

def calculate_depreciation(image_path, brand=None, fabric=None, purchase_date=None, wear_tear_score=0):
    """
        Calculate the depreciation of a clothing item.
        Args: image_path (str): Path to the uploaded image. brand (str): Clothing brand (used to adjust depreciation). fabric (str): Type of fabric (affects depreciation rate). purchase_date (str): Date of purchase in format 'YYYY-MM-DD'. wear_tear_score (float): Wear and tear prediction score (between 0 and 1).
        Returns: dict: A dictionary containing the original price, depreciation rate, and estimated current value. """

    # 1. Predict the age of the clothing item
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # Assuming your TensorFlow model predicts the clothing's age
    prediction = model.predict(img_array)
    estimated_age = prediction[0][0]

    # 2. Calculate base depreciation based on age
    age_depreciation = estimate_age_based_depreciation(estimated_age)


    # 3. Adjust depreciation based on brand
    brand_depreciation_rate = BRAND_DEPRECIATION.get(brand.lower(), 0.1) # Default to 10% if brand is unknown

    # 4. Adjust depreciation based on fabric
    fabric_depreciation_rate = FABRIC_DEPRECIATION.get(fabric.lower(), 0.1) # Default to 10% if fabric is unknown

    # 5. Adjust depreciation based on purchase date (if available)
    if purchase_date:
        try:
            purchase_date_obj = datetime.strptime(purchase_date, '%Y-%m-%d')
            age_in_years = (datetime.now() - purchase_date_obj).days / 365
            age_depreciation = estimate_age_based_depreciation(age_in_years)
        except Exception as e: print(f"Error parsing purchase date: {e}")

    # 6. Combine depreciation factors with wear and tear adjustment
    # Wear and tear is factored into the overall depreciation rate
    final_depreciation_rate = age_depreciation * (1 - brand_depreciation_rate) * (1 - fabric_depreciation_rate) * (1 - wear_tear_score)

    # Assuming we know the original price (can be fetched via API or hardcoded for now)
    original_price = 100 # Placeholder value; should be replaced with API call results
    current_value = original_price * final_depreciation_rate

    # Return the final depreciation results
    return {
        'original_price': original_price,
        'depreciation_rate': final_depreciation_rate,
        'current_value': current_value,
        'estimated_age': estimated_age,
        'wear_and_tear': wear_tear_score,
        'brand': brand,
        'fabric': fabric
    }