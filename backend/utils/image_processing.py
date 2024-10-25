import numpy as np
from tf_keras.preprocessing import image
from tf_keras.applications.vgg16 import preprocess_input

def process_image(image_path, target_size=(224, 224)):
    """ Preprocesses an image to make it ready for model input.
    Args: image_path (str): Path to the image to be processed. target_size (tuple): The target size for resizing the image.
    Returns: numpy.ndarray: Preprocessed image ready for the model. """

    # Load the image from the specified path and resize it
    img = image.load_img(image_path, target_size=target_size)
    # Convert the image to a NumPy array
    img_array = image.img_to_array(img)

    # Add an extra dimension (batch size of 1) to make it compatible with Keras models
    img_array = np.expand_dims(img_array, axis=0)

    # Preprocess the image (scale pixel values, etc.)
    img_array = preprocess_input(img_array)

    return img_array