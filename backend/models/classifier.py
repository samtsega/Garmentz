import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
# Load the MobileNetV2 model from TensorFlow Hub
MODEL_URL = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
model = tf.keras.Sequential([ hub.KerasLayer(MODEL_URL,
input_shape=(224, 224, 3)) ])

# Function to preprocess image
def preprocess_image(image):
    image = Image.open(image)
    image = image.resize((224, 224))
# Resize image for the model
    image = np.array(image) / 255.0
# Normalize to [0, 1]
    image = np.expand_dims(image, axis=0)
# Add batch dimension
    return image

# Predict function using the pretrained model
def predict_image(image):
    processed_image = (
preprocess_image(image))
    predictions = model(processed_image)
    predicted_class = (
np.argmax(predictions, axis=1))

# Map the class index to a label (this will vary based on the dataset/model used)
# Assume we have a predefined list of clothing-related labels
labels = ['t-shirt', 'jeans', 'jacket', 'dress', 'shoes'] # Example classes
return labels[predicted_class[0]]