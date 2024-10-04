import numpy as np
import pandas as pd
from tf_keras.applications import VGG16
from tf_keras.models import Model, Sequential
from tf_keras.layers import Dense, Flatten, Dropout, Input, concatenate
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
from tf_keras.utils import to_categorical
from datetime import datetime

# 1. Load the pre-trained VGG16 model (for image feature extraction)
vgg16 = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the VGG16 layers (do not retrain them)
vgg16.trainable = False

# Flatten the VGG16 output
image_model = Sequential([
    vgg16,
    Flatten()
])

# 2. Load the metadata (e.g., brand, fabric, age) from CSV
data = pd.read_csv('path_to_your_csv/data.csv')

# 3. Preprocess the metadata
# Convert purchase date to age (years)
data['age'] = data['purchase_date'].apply(lambda x: (datetime.now() - datetime.strptime(x, '%Y-%m-%d')).days / 365)

# Label encode categorical features like brand and fabric
label_encoder_brand = LabelEncoder()
label_encoder_fabric = LabelEncoder()

data['brand_encoded'] = label_encoder_brand.fit_transform(data['brand'])
data['fabric_encoded'] = label_encoder_fabric.fit_transform(data['fabric'])

# 4. Split metadata features (age, brand_encoded, fabric_encoded) and target (depreciation)
metadata_features = data[['age', 'brand_encoded', 'fabric_encoded']].values
target_depreciation = data['depreciation'].values

# 5. Create an input layer for metadata
metadata_input = Input(shape=(metadata_features.shape[1],))

# 6. Combine image and metadata models
# Concatenate the outputs of the image and metadata models
combined = concatenate([image_model.output, metadata_input])

# 7. Add fully connected layers for regression (predict depreciation)
x = Dense(128, activation='relu')(combined)
x = Dropout(0.5)(x)
x = Dense(64, activation='relu')(x)
output = Dense(1, activation='linear')(x) # Linear output for regression

# 8. Build the full model
model = Model(inputs=[image_model.input, metadata_input], outputs=output)

# Compile the model for regression
model.compile(optimizer=Adam(learning_rate=0.0001), loss='mean_squared_error')

# 9. Set up image data generator (to load and augment images)
image_datagen = ImageDataGenerator(rescale=1.0 / 255)

# Flow the image data from the directory specified in the CSV
train_image_generator = image_datagen.flow_from_dataframe(
    dataframe=data,
    directory="path_to_image_directory",
    x_col="image_path",
    y_col=None,
    target_size=(224, 224),
    batch_size=32,
    class_mode=None
)

# 10. Train the model
model.fit(
    [train_image_generator, metadata_features],
    target_depreciation,
    epochs=5, # Adjust epochs as needed
    batch_size=32 )

# 11. Save the trained model as an .h5 file

model.save('models/depreciation_model.h5')