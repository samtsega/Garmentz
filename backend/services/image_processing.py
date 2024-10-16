import numpy as np
from PIL import Image
import tensorflow as tf_keras
import os

# Load your trained model (ensure the path is correct)
model = tf_keras.models.load_model('path/to/clothing_model.h5')


def load_image(image_path):
    """Load an image from the specified path."""
    try:
        img = Image.open(image_path)
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def preprocess_image(image, target_size=(224, 224)):
    """Resize and preprocess the image for the model."""
    # Resize the image
    img = image.resize(target_size)

    # Convert to array and normalize
    img_array = np.array(img) / 255.0

    # If your model expects a bat
