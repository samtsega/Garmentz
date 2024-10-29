from flask import Flask, request,jsonify, redirect, url_for, render_template, session
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from tf_keras.models import load_model
from werkzeug.utils import secure_filename
import numpy as np
import os
from dotenv import load_dotenv
from services.image_processing import load_and_preprocess_image
from utils.currency_conversions import convert_currency
from services.depreciation_service import calculate_depreciation

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config["APP_NAME"] = "https://garmentz1-fa5d7c6634fb.herokuapp.com/"

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

app.secret_key = 'your_secret_key'  # Replace with your actual secret key
oauth = OAuth(app)

# Register OAuth clients for Google, Facebook, and Twitter
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/google/callback',
    client_kwargs={'scope': 'openid profile email'}
)

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/google/callback',
    client_kwargs={'scope': 'openid profile email'}
)

oauth.register(
    name='facebook',
    client_id=os.getenv('FACEBOOK_CLIENT_ID'),
    client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
    authorize_url='https://www.facebook.com/dialog/oauth',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    redirect_uri='http://localhost:5000/facebook/callback',
    client_kwargs={'scope': 'email public_profile'}
)

oauth.register(
    name='twitter',
    client_id=os.getenv('TWITTER_CLIENT_ID'),
    client_secret=os.getenv('TWITTER_CLIENT_SECRET'),
    request_token_url='https://api.twitter.com/oauth/request_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    access_token_url='https://api.twitter.com/oauth/access_token',
    redirect_uri='http://localhost:5000/twitter/callback',
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/<provider>')
def login(provider):
    provider_oauth = oauth.create_client(provider)
    redirect_uri = url_for(f'{provider}_callback', _external=True)
    return provider_oauth.authorize_redirect(redirect_uri)

@app.route('/google/callback')
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    session['user'] = user_info
    return redirect('/dashboard')

@app.route('/facebook/callback')
def facebook_callback():
    token = oauth.facebook.authorize_access_token()
    user_info = oauth.facebook.get('me?fields=id,name,email,picture').json()
    session['user'] = user_info
    return redirect('/dashboard')

@app.route('/twitter/callback')
def twitter_callback():
    token = oauth.twitter.authorize_access_token()
    user_info = oauth.twitter.get('account/verify_credentials.json').json()
    session['user'] = user_info
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect('/')
    return f"Hello, {user['name']}!"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/account-deletion', methods=['POST'])
def account_deletion():
    # Check for challenge code for verification
    challenge_code = request.headers.get('challenge-code')

    # If it's a verification request
    if challenge_code:
        # Respond to eBay with the challenge code
        return jsonify({'challengeResponse': challenge_code}), 200

    # Handle the account deletion notification
    data = request.json
    print("Received account deletion notification:", data)

    # Implement logic to delete the user's data from your system here

@app.route('/marketplace-account-deletion', methods=['POST'])
def marketplace_account_deletion():
    notification_data = request.json  # Get the JSON data sent from eBay
    # Process the notification data as needed
    print(notification_data)  # For debugging
    return '', 200  # Respond with a 200 OK status

# Define upload folder and allowed extensions
UPLOAD_FOLDER = 'backend.upload/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['backend.upload'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if the uploaded file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask route to handle image upload
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the image by passing its path
        preprocessed_image = load_and_preprocess_image(file_path)

        if preprocessed_image is not None:
            # You can now use this preprocessed image for prediction or other tasks
            # For example, you might load a model and make predictions here
            # model = load_model('clothing_model.h5')
            # predictions = model.predict(preprocessed_image)

            return jsonify({'message': 'Image uploaded and processed successfully'}), 200
        else:
            return jsonify({'error': 'Image preprocessing failed'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400


# Load the trained model
wear_and_tear_model = load_model('models/wear_and_tear_model.h5')

@app.route('/predict-wear-tear', methods=['POST'])
def predict_wear_tear():
    # Expect an image file in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    image_file = request.files['image']
    image_array = load_and_preprocess_image(image_file)

    # Use the loaded model to predict wear and tear
    prediction = wear_and_tear_model.predict(image_array)
    predicted_wear_tear = np.argmax(prediction)

    # Get the predicted class index
    return jsonify({'predicted_wear_tear': int(predicted_wear_tear)})
@app.route('/convert-currency', methods=['POST'])
def convert_currency_endpoint():
    data = request.json
    amount = data['amount']
    source_currency = data['source_currency']
    target_currency = data['target_currency']

    # Call the currency conversion service
    converted_amount = convert_currency(amount, source_currency, target_currency)

    return jsonify({'converted_amount': converted_amount})
@app.route('/calculate-depreciation', methods=['POST'])
def calculate_depreciation_endpoint():
    data = request.json
    image_file = request.files['image']
    brand = data.get('brand')
    fabric = data.get('fabric')
    purchase_date = data.get('purchase_date')
    target_currency = data.get('target_currency')
    image_array = load_and_preprocess_image(image_file)

    # Predict depreciation based on the image and other details
    depreciation_data = calculate_depreciation( image_array, brand, fabric, purchase_date, target_currency )
    return jsonify(depreciation_data)
if __name__ == '__main__': app.run(debug=True)