import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json

# 1. Load and Preprocess Data
def load_wear_and_tear_data(data_dir, image_size=(128, 128)):
    """
    Loads image data and labels from the dataset directories.
    Returns the images and labels ready for model training.
    """
    categories = ['heavily_worn', 'lightly_worn', 'new']
    data = []
    labels = []

    for category in categories:
        category_path = os.path.join(data_dir, category)
        label = categories.index(category)  # Assign label 0 for heavily worn, 1 for lightly worn, and 2 for new
        
        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)
            # If working with images, load and resize them
            image = tf.keras.preprocessing.image.load_img(file_path, target_size=image_size)
            image = tf.keras.preprocessing.image.img_to_array(image)
            image = image / 255.0  # Normalize pixel values

            # Add image and corresponding label to the dataset
            data.append(image)
            labels.append(label)

    # Convert lists to numpy arrays
    return np.array(data), np.array(labels)

# 2. Build the Model (CNN for image data)
def build_wear_and_tear_model(input_shape):
    """
    Builds and returns a CNN model for wear and tear classification.
    """
    model = models.Sequential()

    # Convolutional layers
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    # Flatten and fully connected layers
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(3, activation='softmax'))  # 3 output classes (heavily worn, lightly worn, new)

    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model

# 3. Train the Model
def train_wear_and_tear_model(data_dir):
    """
    Loads data, builds the model, and trains it.
    """
    # Load and preprocess data
    image_size = (128, 128)  # Resize all images to 128x128
    X, y = load_wear_and_tear_data(data_dir, image_size=image_size)

    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define data augmentation (to prevent overfitting)
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True
    )

    # Build the CNN model
    model = build_wear_and_tear_model(input_shape=(image_size[0], image_size[1], 3))  # 3 for RGB channels

    # Train the model
    history = model.fit(datagen.flow(X_train, y_train, batch_size=32),
                        validation_data=(X_val, y_val),
                        epochs=10)

    # Save the trained model to a file
    model.save('wear_and_tear_model.h5')

    return model

# 4. Predict Wear and Tear
def predict_wear_and_tear(image_path):
    """
    Loads the trained model and predicts wear and tear level for a given image.
    """
    # Load the saved model
    model = tf.keras.models.load_model('wear_and_tear_model.h5')

    # Preprocess the input image
    image_size = (128, 128)
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=image_size)
    image = tf.keras.preprocessing.image.img_to_array(image) / 255.0  # Normalize pixel values
    image = np.expand_dims(image, axis=0)  # Add batch dimension

    # Predict the wear and tear category
    prediction = model.predict(image)
    wear_and_tear_categories = ['heavily worn', 'lightly worn', 'new']

    return wear_and_tear_categories[np.argmax(prediction)]

# 5. Example Usage
if __name__ == "__main__":
    # Example data directory path (replace with your actual dataset path)
    data_dir = '/path/to/data'

    # Train the model
    train_wear_and_tear_model(data_dir)

    # Predict wear and tear on a new item (replace with actual image path)
    prediction = predict_wear_and_tear('/path/to/new/image.jpg')
    print(f"Predicted wear and tear category: {prediction}")