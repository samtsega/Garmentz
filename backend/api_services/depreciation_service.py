import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from datetime import datetime

# Load your trained depreciation TensorFlow model
MODEL_PATH = os.getenv('DEPRECIATION_MODEL_PATH', 'models/depreciation_model.h5')
model = load_model(MODEL_PATH)

# A dictionary or database of average depreciation rates based on brand or fabric
BRAND_DEPRECIATION = {
    'brand_a': 0.1, # 10% depreciation per year
    'brand_b': 0.2, # 20% depreciation per year
    'brand_c': 0.15 # 15% depreciation per year
}
FABRIC_DEPRECIATION = {
    'cotton': 0.1,
    'leather': 0.05,
    'polyester': 0.2,
    'wool': 0.07
}

def preprocess_image(image_path): """ Preprocesses an image for TensorFlow model input. """
img = image.load_img(image_path, target_size=(224, 224)) # Resize to match the input shape expected by your model
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
img_array = preprocess_input(img_array) # VGG16 preprocess (if you're using a similar model)
return img_array

def estimate_age_based_depreciation(age):
""" Estimate depreciation based on the clothing's age. """
# Simple linear depreciation by age; can be customized further.
depreciation_rate_per_year = 0.1
# Assume 10% depreciation per year as a base
return 1 - (depreciation_rate_per_year * age)

def calculate_depreciation(image_path, brand=None, fabric=None, purchase_date=None):
""" Calculate the depreciation of a clothing item.
Args:
    image_path (str): Path to the uploaded image.
    brand (str): Clothing brand (used to adjust depreciation).
    fabric (str): Type of fabric (affects depreciation rate).
    purchase_date (str): Date of purchase in format 'YYYY-MM-DD'.
Returns:
    dict: A dictionary containing the original price, depreciation rate, and estimated current value. """

# 1. Predict features from the image (if using image recognition for extra data)
img = preprocess_image(image_path)

# Assuming your TensorFlow model outputs a probability or features for the clothing
prediction = model.predict(img)

# Let's assume the model predicts the age in years (as an example)
estimated_age = prediction[0][0] # First output node is the age prediction in years

# 2. Calculate base depreciation based on age
age_depreciation = estimate_age_based_depreciation(estimated_age)

# 3. Adjust depreciation based on brand
brand_depreciation_rate = BRAND_DEPRECIATION.get(brand.lower(), 0.1) # Default to 10% per year if unknown brand

# 4. Adjust depreciation based on fabric
fabric_depreciation_rate = FABRIC_DEPRECIATION.get(fabric.lower(), 0.1) # Default to 10% if unknown fabric

# 5. Additional adjustment based on purchase date (if available)
if purchase_date:
    try:
        purchase_date_obj = datetime.strptime(purchase_date, '%Y-%m-%d')
        age_in_years = (datetime.now() - purchase_date_obj).days / 365
        age_depreciation = estimate_age_based_depreciation(age_in_years)
    except Exception as e: print(f"Error parsing purchase date: {e}")

# 6. Combine depreciation factors
final_depreciation_rate = age_depreciation * (1 - brand_depreciation_rate) * (1 - fabric_depreciation_rate)

# Assuming we know the original price, let's calculate the current value
original_price = 100 # Just a placeholder for now. In a real app, you may fetch this from an external API.
current_value = original_price * final_depreciation_rate

# Return the results
return {
    'original_price': original_price,
    'depreciation_rate': final_depreciation_rate,
    'current_value': current_value,
    'estimated_age': estimated_age,
    'brand': brand, 'fabric': fabric
}