import numpy as np
import os
import scipy
import pandas as pd
import tensorflow as tf
from tf_keras.applications import VGG16
from tf_keras.layers import Dense, Flatten, Dropout
from tf_keras.models import Sequential
from tf_keras.optimizers import Adam
from tf_keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

# Set paths
csv_path = '/Users/samitsega/PycharmProjects/GarmentzCode/backend/metadata/csv/dataset.csv'
validation_csv_path = '/Users/samitsega/PycharmProjects/GarmentzCode/backend/metadata/validation/validation.csv'
image_dir = '/Users/samitsega/PycharmProjects/GarmentzCode/backend/image_dataset_dir'  # Directory containing images

# Load CSV data
data = pd.read_csv(csv_path)
validation_data = pd.read_csv(validation_csv_path)

# Confirm required columns exist
required_columns = ['image_name', 'wear_category', 'clothing_type', 'fabric_type', 'wear_signs']
for col in required_columns:
    if col not in data.columns or col not in validation_data.columns:
        raise ValueError(f"CSV files must contain '{col}' column")

# Ensure TensorFlow version is correct
print(f"Using TensorFlow version: {tf.__version__}")

# Load pretrained VGG16 model, excluding the top layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze the base model

# Build and compile the model
model = Sequential([
    base_model,
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(len(data['wear_category'].unique()), activation='softmax')  # Adjusted for the number of unique categories
])
model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Map wear categories to numerical labels
category_mapping = {category: idx for idx, category in enumerate(data['wear_category'].unique())}

# Define a function to load images and labels
def load_images_and_labels(df, image_dir):
    images = []
    labels = []
    for idx, row in df.iterrows():
        img_path = os.path.join(image_dir, row['image_name'])  # Directly use image_name
        if os.path.exists(img_path):
            img = load_img(img_path, target_size=(224, 224))
            img_array = img_to_array(img) / 255.0
            images.append(img_array)
            # Map the wear_category to numerical labels using category_mapping
            wear_category = row['wear_category'].strip()  # Ensure no leading/trailing spaces
            if wear_category in category_mapping:
                labels.append(category_mapping[wear_category])  # Append the numerical label
            else:
                print(f"Warning: Unknown wear category '{wear_category}' for image {img_path}.")
        else:
            print(f"Warning: Image {img_path} not found.")
    return np.array(images), np.array(labels)

# Load images and labels for training and validation sets
train_images, train_labels = load_images_and_labels(data, image_dir)
val_images, val_labels = load_images_and_labels(validation_data, image_dir)

# Set up ImageDataGenerator for augmentation
train_datagen = ImageDataGenerator(
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Create generators for the loaded images
train_generator = train_datagen.flow(train_images, train_labels, batch_size=32)
validation_generator = ImageDataGenerator().flow(val_images, val_labels, batch_size=32)

# Combine training and validation images and labels for reusability
combined_images = np.concatenate((train_images, val_images))
combined_labels = np.concatenate((train_labels, val_labels))

# Set up ImageDataGenerator for augmentation (you can also add any additional augmentations)
train_datagen = ImageDataGenerator(
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Create a generator for the combined dataset
combined_generator = train_datagen.flow(combined_images, combined_labels, batch_size=32)

# Train the model
model.fit(
    combined_generator,
    steps_per_epoch=len(combined_images) // 32,  # Use the combined dataset length for steps
    epochs=10
)

# Save the model
model.save('wear_and_tear_model.h5')
print("Model saved as wear_and_tear_model.h5")


# Save the model
model.save('wear_and_tear_model.h5')
print("Model saved as wear_and_tear_model.h5")

# Function to predict wear and tear score for a new image
def predict_wear_and_tear(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    wear_tear_score = model.predict(img_array)
    return np.argmax(wear_tear_score[0])  # Returns the predicted class index
