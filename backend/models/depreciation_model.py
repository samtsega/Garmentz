import pandas as pd
import requests
from tf_keras.applications import VGG16
from tf_keras.models import Model, Sequential
from tf_keras.layers import Dense, Flatten, Dropout, Input, concatenate
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# eBay API credentials
app_id = 'Garmentz-Garmentz-PRD-fb1427ba0-69aaf28d'  # Replace with your App ID
client_secret = 'YOUR_CLIENT_SECRET'  # Replace with your Client Secret
refresh_token = 'YOUR_REFRESH_TOKEN'  # Replace with your Refresh Token
base_url = 'https://api.ebay.com'


# Function to obtain OAuth token
def get_oauth_token():
    url = 'https://api.ebay.com/identity/v1/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    response = requests.post(url, headers=headers, auth=(app_id, client_secret), data=data)

    if response.status_code == 200:
        return response.json().get('access_token')  # Extract access token
    else:
        print(f"Error obtaining token: {response.status_code} - {response.text}")
        return None


# Function to retrieve item details from eBay using the Buy API
def get_ebay_item_details(item_id):
    token = get_oauth_token()  # Get the OAuth token
    if not token:
        return None

    url = f"{base_url}/buy/browse/v1/item/{item_id}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return JSON response if successful
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# 1. Fetch item IDs from your eBay listings directory
# Assuming you have a file or list of item IDs stored, e.g., in a text file or another CSV
item_ids = [
    'ITEM_ID_1',  # Replace with actual eBay item IDs
    'ITEM_ID_2',
    'ITEM_ID_3'
]  # This should be fetched or read from your data source

# 2. Create an empty list to hold metadata
data = []

# 3. Fetch purchase dates and other details from eBay API
for item_id in item_ids:
    item_details = get_ebay_item_details(item_id)

    if item_details:
        purchase_date = item_details.get('itemMarketplace', {}).get('purchaseDate',
                                                                    None)  # Adjust based on API response
        brand = item_details.get('brand', None)  # Adjust based on API response
        fabric = item_details.get('fabric', None)  # Adjust based on API response
        depreciation = item_details.get('depreciation', None)  # Adjust based on API response

        # Append the details to the data list
        data.append({
            'item_id': item_id,
            'purchase_date': purchase_date,
            'brand': brand,
            'fabric': fabric,
            'depreciation': depreciation
        })

# Convert the list to a DataFrame
data = pd.DataFrame(data)

# 4. Preprocess the metadata
# Convert purchase date to age (years)
data['age'] = data['purchase_date'].apply(lambda purchase_date: (datetime.now() - datetime.strptime(purchase_date,
                                                                                                    '%Y-%m-%d')).days / 365 if purchase_date else None)

# Label encode categorical features like brand and fabric
label_encoder_brand = LabelEncoder()
label_encoder_fabric = LabelEncoder()

data['brand_encoded'] = label_encoder_brand.fit_transform(data['brand'])
data['fabric_encoded'] = label_encoder_fabric.fit_transform(data['fabric'])

# 5. Split metadata features (age, brand_encoded, fabric_encoded) and target (depreciation)
metadata_features = data[['age', 'brand_encoded', 'fabric_encoded']].values
target_depreciation = data['depreciation'].values

# 6. Create an input layer for metadata
metadata_input = Input(shape=(metadata_features.shape[1],))

# 7. Load the pre-trained VGG16 model (for image feature extraction)
vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the VGG16 layers (do not retrain them)
vgg16.trainable = False

# Flatten the VGG16 output
image_model = Sequential([
    vgg16,
    Flatten()
])

# 8. Combine image and metadata models
# Concatenate the outputs of the image and metadata models
combined = concatenate([image_model.output, metadata_input])

# 9. Add fully connected layers for regression (predict depreciation)
x = Dense(128, activation='relu')(combined)
x = Dropout(0.5)(x)
x = Dense(64, activation='relu')(x)
output = Dense(1, activation='linear')(x)  # Linear output for regression

# 10. Build the full model
model = Model(inputs=[image_model.input, metadata_input], outputs=output)

# Compile the model for regression
model.compile(optimizer=Adam(learning_rate=0.0001), loss='mean_squared_error')

# 11. Set up image data generator (to load and augment images)
image_datagen = ImageDataGenerator(rescale=1.0 / 255)

# Flow the image data from the directory specified in the CSV
train_image_generator = image_datagen.flow_from_dataframe(
    dataframe=data,
    directory="/Users/samitsega/PycharmProjects/GarmentzCode/backend/image_dataset_dir",
    x_col="image_path",
    y_col=None,
    target_size=(224, 224),
    batch_size=32,
    class_mode=None
)

# 12. Train the model
model.fit(
    [train_image_generator, metadata_features],
    target_depreciation,
    epochs=5,  # Adjust epochs as needed
    batch_size=32
)

# 13. Save the trained model as an .h5 file
model.save('models/depreciation_model.h5')
