import os
import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from depreciation_service import calculate_depreciation
from currency_conversion import convert_currency
from image_processing import process_image
from wear_tear_model import predict_wear_and_tear

# Import the wear and tear prediction function
app = Flask(__name__)

# Configure the upload folder for images
app.config['UPLOAD_FOLDER'] = 'path_to_your_upload_directory'

# Helper function to get the original price of the clothing item from different platforms
def get_original_price(brand, product_id, platform):
    """ This function calls external APIs to get the original price of the item based on the platform.
    Args: brand (str): The brand of the clothing item. product_id (str): The unique product identifier (SKU or item number).
    platform (str): The platform from which to retrieve the price (Amazon, eBay, Depop, etc.).
    Returns: float: The original price of the item. """
    if platform == 'amazon':
        amazon_api_url = f"https://api.amazon.com/product/{product_id}/price"
        response = requests.get(amazon_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    elif platform == 'ebay':
        ebay_api_url = f"https://api.ebay.com/item/{product_id}/price"
        response = requests.get(ebay_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    elif platform == 'depop':
        depop_api_url = f"https://api.depop.com/product/{product_id}/price"
        response = requests.get(depop_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    elif platform == 'vestiaire':
        vestiaire_api_url = f"https://api.vestiaire.com/product/{product_id}/price"
        response = requests.get(vestiaire_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    elif platform == 'farfetch':
        farfetch_api_url = f"https://api.farfetch.com/product/{product_id}/price" #implement real api url later
        response = requests.get(farfetch_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    elif platform == 'grailed':
        grailed_api_url = f"https://api.grailed.com/product/{product_id}/price"  # implement real api url later
        response = requests.get(grailed_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    elif platform == 'fashionphile':
        farfetch_api_url = f"https://api.fashionphile.com/product/{product_id}/price"  # implement real api url later
        response = requests.get(fashionphile_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    elif platform == 'saksfifth':
        saksfifth_api_url = f"https://api.saksfifth.com/product/{product_id}/price"  # implement real api url later
        response = requests.get(saksfifth_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    elif platform == 'ssense':
        ssense_api_url = f"https://api.ssense.com/product/{product_id}/price"  # implement real api url later
        response = requests.get(ssense_api_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('price', 0)

    return 0 # Return 0 if no valid response





@app.route('/calculate_depreciation', methods=['POST'])
def calculate_depreciation_route():
    """
    API route to handle the full workflow:
    1. Image Processing to extract features
    2. API Requests to fetch original prices
    3. Depreciation Calculation with wear and tear model
    4. Currency Conversion """

    # Handle form data from the request
    brand = request.form.get('brand')
    fabric = request.form.get('fabric')
    purchase_date = request.form.get('purchase_date')
    platform = request.form.get('platform') # Example: Amazon, eBay, Depop, Vestiaire
    product_id = request.form.get('product_id')
    target_currency = request.form.get('target_currency', 'USD')

    # Handle the image file upload
    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Step 1: Process the uploaded image
    image_features = process_image(filepath) # Call your image processing function
    print(f"Image processed: {image_features}")

    # Step 2: Predict wear and tear using the trained model
    wear_tear_score = predict_wear_and_tear(filepath) # Predict wear and tear percentage
    print(f"Wear and Tear: {wear_tear_score * 100}%")

    # Step 3: Fetch the original price from the selected platform using the product_id
    original_price = get_original_price(brand, product_id, platform)
    print(f"Original Price: {original_price}")

    # Step 4: Calculate depreciation based on age, brand, fabric, and predicted wear and tear
    depreciation_result = calculate_depreciation(filepath, brand, fabric, purchase_date, wear_tear_score)
    current_value_in_usd = depreciation_result['current_value']
    print(f"Current Value (USD): {current_value_in_usd}")

    # Step 5: Convert the current value into the target currency
    converted_value = convert_currency(current_value_in_usd, 'USD', target_currency)
    print(f"Converted Value ({target_currency}): {converted_value}")

    # Prepare the final result to return as a response
    result = {
        'original_price': original_price,
        'depreciation_rate': depreciation_result['depreciation_rate'],
        'current_value': current_value_in_usd,
        'converted_value': converted_value,
        'currency': target_currency,
        'estimated_age': depreciation_result['estimated_age'],
        'wear_and_tear': wear_tear_score,
        'brand': brand,
        'fabric': fabric,
        'platform': platform }

    return jsonify(result)

if __name__ == '__main__': app.run(debug=True)
