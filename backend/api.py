import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from ebay_service import fetch_ebay_data
from depop_service import fetch_depop_data
from vestiaire_service import fetch_vestiaire_data
from grailed_service import fetch_grailed_data
from farfetch_service import fetch_farfetch_data
from saksfifth_service import fetch_saksfifth_data
from fashionphile_service import fetch_fashionphile_data
from amazon_service import fetch_amazon_data
from ssense_service import fetch_ssense_data
from util import process_image from currency_conversion
import (convert_price) # Import currency conversion module

app = Flask(__name__)

# Set upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename): """Check if the uploaded file is an image and has a valid extension."""
return '.' in filename and filename.rsplit('.', 1)[1].lower() in
ALLOWED_EXTENSIONS @app.route('/upload', methods=['POST'])
def upload_image(): """Endpoint to upload an image and calculate depreciation."""
if 'image' not in request.files:
    return jsonify({'error': 'No image part in the request'}), 400 file = request.files['image']
if file.filename == '': return jsonify({'error': 'No image selected for uploading'}), 400
if file and allowed_file(file.filename): filename = secure_filename(file.filename)
filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) file.save(filepath)

# Process the uploaded image using a TensorFlow model
processed_image = process_image(filepath)

# Optionally, you can get extra details like brand, fabric from the request
brand = request.form.get('brand')
fabric = request.form.get('fabric')
purchase_date = request.form.get('purchase_date')

# Calculate depreciation based on image, brand, and fabric
depreciation_data = calculate_depreciation(filepath, brand, fabric, purchase_date)
return jsonify(depreciation_data)
else: return jsonify({'error': 'Allowed image types are -> png, jpg, jpeg'}), 400
def handle_currency_conversion(data, original_currency, target_currency): """Convert prices in the fetched data to the target currency."""
if original_currency != target_currency:
    for item in data: item['price'] = convert_price(item['price'], original_currency, target_currency)
    return data @app.route('/search/ebay', methods=['GET'])
    def search_ebay(): """Endpoint to search for items on eBay."""
    query = request.args.get('query')
    original_currency = request.args.get('original_currency', 'USD')
    target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({'error': 'Query parameter is required'}), 400

# Fetch eBay data
ebay_data = fetch_ebay_data(query)
if ebay_data:
    ebay_data = handle_currency_conversion(ebay_data, original_currency, target_currency)
    return jsonify(ebay_data)
else:
    return jsonify({'error': 'No items found on eBay'}), 404
@app.route('/search/depop', methods=['GET'])
def search_depop(): """Endpoint to search for items on Depop."""
query = request.args.get('query')
original_currency = request.args.get('original_currency', 'USD')
target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({'error': 'Query parameter is required'}), 400

# Fetch Depop data

depop_data = fetch_depop_data(query)
if depop_data:
    depop_data = handle_currency_conversion(depop_data, original_currency, target_currency)
    return jsonify(depop_data)
else: return jsonify({'error': 'No items found on Depop'}), 404

# Similarly update other search routes with currency conversion:
@app.route('/search/vestiaire', methods=['GET'])
def search_vestiaire():
"""Endpoint to search for items on Vestiaire Collective."""
query = request.args.get('query')
original_currency = request.args.get('original_currency', 'USD')
target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({'error': 'Query parameter is required'}), 400

# Fetch Vestiaire data
vestiaire_data = fetch_vestiaire_data(query)
if vestiaire_data:
    vestiaire_data = handle_currency_conversion(vestiaire_data, original_currency, target_currency)
return jsonify(vestiaire_data)
else: return jsonify({'error': 'No items found on Vestiaire Collective'}), 404

# Fetch Grailed data

@app.route('/search/grailed', methods=['GET'])
def search_grailed(): """Endpoint to search for items on Grailed."""
query = request.args.get('query')
original_currency = request.args.get('original_currency', 'USD')
target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({'error': 'Query parameter is required'}), 400

# Fetch Grailed data
grailed_data = fetch_grailed_data(query)
if grailed_data:
    grailed_data = handle_currency_conversion(grailed_data, original_currency, target_currency)
    return jsonify(grailed_data)
else:
    return jsonify({'error': 'No items found on Grailed'}), 404

# Fetch Amazon data

@app.route('/search/amazon', methods=['GET'])
def search_amazon(): """Endpoint to search for items on Amazon."""
query = request.args.get('query')
original_currency = request.args.get('original_currency', 'USD')
target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({'error': 'Query parameter is required'}), 400

# Fetch Amazon data
amazon_data = fetch_amazon_data(query)
if amazon_data:
    amazon_data = handle_currency_conversion(amazon_data, original_currency, target_currency)
return jsonify(amazon_data)
else: return jsonify({'error': 'No items found on Amazon'}), 404

# Fetch Farfetch data

@app.route('/search/farfetch', methods=['GET'])
def search_farfetch(): """Endpoint to search for items on Amazon."""
query = request.args.get('query')
original_currency = request.args.get('original_currency', 'USD')
target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({'error': 'Query parameter is required'}), 400

# Fetch Farfetch data
farfetch_data = fetch_farfetch_data(query)
if farfetch_data:
    farfetch_data = handle_currency_conversion(farfetch_data, original_currency, target_currency)
    return jsonify(farfetch_data)
else:
    return jsonify({'error': 'No items found on Farfetch'}), 404

# Fetch Fashionphile data
@app.route('/search/fashionphile', methods=['GET'])
def search_farfetch(): """Endpoint to search for items on Fashionphile."""
query = request.args.get('query')
original_currency = request.args.get('original_currency', 'USD')
target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({'error': 'Query parameter is required'}), 400

# Fetch Fashionphile data
fashionphile_data = fetch_fashionphile_data(query)
if fashionphile_data:
    fashionphile_data = handle_currency_conversion(fashionphile_data, original_currency, target_currency)
    return jsonify(fashionphile_data)
else:
    return jsonify({'error': 'No items found on Fashionphile'}), 404

# Fetch Saks Fifth data
@app.route('/search/saksfifth', methods=['GET'])
def search_saksfifth(): """Endpoint to search for items on Saks Fifth."""
query = request.args.get('query')
original_currency = request.args.get('original_currency', 'USD')
target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({
        'error': 'Query parameter is required'}), 400

# Fetch SaksFifth data
saksfifth_data = fetch_saksfifth_data(query)
if saksfifth_data:
    saksfifth_data = handle_currency_conversion(fashionphile_data, original_currency, target_currency)
    return jsonify(saksfifth_data)
else:
    return jsonify({'error': 'No items found on Saks Fifth'}), 404

# Fetch Ssense data
@app.route('/search/sssense', methods=['GET'])
def search_ssense(): """Endpoint to search for items on Ssense."""
query = request.args.get('query')
original_currency = request.args.get('original_currency', 'USD')
target_currency = request.args.get('target_currency', 'USD')
if not query:
    return jsonify({
        'error': 'Query parameter is required'}), 400

# Fetch Ssense data
ssense_data = fetch_sssense_data(query)
if sssense_data:
    sssense_data = handle_currency_conversion(ssense_data, original_currency, target_currency)
    return jsonify(ssense_data)
else:
    return jsonify({'error': 'No items found on Ssense'}), 404

if __name__ == '__main__': app.run(debug=True)