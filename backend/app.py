import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from depreciation_service import calculate_depreciation
from currency_conversions import convert_price # Import the currency conversion function

app = Flask(__name__)

# Set up an upload folder for the images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """ Check if the file has an allowed extension. """
return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/scan', methods=['POST'])
def scan_clothing():
    """ API route to handle the clothing scan and depreciation calculation. """
if 'image' not in request.files:
return jsonify({'error': 'No image file provided'}), 400
image = request.files['image']

if image.filename == '': return jsonify({'error': 'No selected file'}), 400
if not allowed_file(image.filename): return jsonify({'error': 'File type not allowed'}), 400

# Save the uploaded image
filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)) image.save(filepath)

# Get additional data (brand, fabric, purchase date, original and target currency) from the form
brand = request.form.get('brand')
fabric = request.form.get('fabric')
purchase_date = request.form.get('purchase_date')
original_currency = request.form.get('original_currency', 'USD') # Default to USD if not provided
target_currency = request.form.get('target_currency', 'USD') # Default to USD if not provided

# Get original and current prices from the form
original_price = float(request.form.get('original_price'))
current_price = float(request.form.get('current_price'))

# Convert the prices to the target currency
converted_original_price = convert_price(original_price, original_currency, target_currency)
converted_current_price = convert_price(current_price, original_currency, target_currency)

# Call the depreciation service to calculate depreciation using converted prices
depreciation_data = calculate_depreciation(filepath, brand, fabric, purchase_date, converted_original_price, converted_current_price)

# Include the converted prices and currency in the response
depreciation_data['converted_original_price'] = converted_original_price
depreciation_data['converted_current_price'] = converted_current_price
depreciation_data['currency'] = target_currency

return jsonify(depreciation_data)

if __name__ == '__main__':
# Run the Flask app on localhost, port 5000 (default settings)
app.run(debug=True)