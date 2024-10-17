import tensorflow as tf_keras
import numpy as np
import logging
from PIL import Image

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_and_preprocess_image(image_path, target_size=(150, 150)):
    """
    Load an image from file and preprocess it for model prediction.

    :param image_path: Path to the image file.
    :param target_size: Tuple specifying the target size (width, height) for resizing the image.
    :return: Preprocessed image ready for model prediction.
    """
    try:
        # Load the image using TensorFlow
        image = tf_keras.io.read_file(image_path)
        image = tf_keras.image.decode_image(image, channels=3)  # Ensure image has 3 channels (RGB)

        # Resize the image to the target size
        image = tf_keras.image.resize(image, target_size)

        # Normalize the pixel values (scale to [0, 1])
        image = image / 255.0

        # Expand dimensions to match model input (e.g., (1, 150, 150, 3) for batch size of 1)
        image = tf_keras.expand_dims(image, axis=0)

        logger.info(f"Successfully loaded and preprocessed image: {image_path}")
        return image

    except Exception as e:
        logger.error(f"Error loading or processing image {image_path}: {e}")
        return None


def predict_image_class(model, image_path):
    """
    Predict the class of an image using a trained model.

    :param model: Trained TensorFlow model.
    :param image_path: Path to the image file.
    :return: Predicted class and confidence score.
    """
    # Load and preprocess the image
    processed_image = load_and_preprocess_image(image_path)

    if processed_image is not None:
        # Make predictions
        predictions = model.predict(processed_image)

        # Get the predicted class (assuming a classification model)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence_score = np.max(predictions, axis=1)[0]

        logger.info(f"Predicted class: {predicted_class}, Confidence: {confidence_score:.2f}")
        return predicted_class, confidence_score
    else:
        logger.error("Failed to process image for prediction.")
        return None, None


# Example usage of the functions
if __name__ == '__main__':
    # Load your trained model (make sure to specify the correct path to your model)
    model = tf_keras.models.load_model('clothing_model.h5')

    # Path to the image you want to predict
    image_path = 'path/to/your/image.jpg'

    predicted_class, confidence_score = predict_image_class(model, image_path)
    print(f"Predicted class: {predicted_class}, Confidence: {confidence_score:.2f}")
