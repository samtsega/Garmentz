import os
import numpy as np
from PIL import Image
from tf_keras.preprocessing import image
from tf_keras.applications.vgg16 import preprocess_input

# Directory to save processed images
PROCESSED_IMAGES_DIR = 'processed_images'
if not os.path.exists(PROCESSED_IMAGES_DIR):
        os.makedirs(PROCESSED_IMAGES_DIR)
def save_image(img_array, filename):
    """ Save the processed image array back to disk. """
img = Image.fromarray(np.uint8(img_array))
img.save(os.path.join(PROCESSED_IMAGES_DIR, filename))

def preprocess_image(image_path):
    """ Preprocesses an image for TensorFlow model input. """

# Load the image using PIL
img = Image.open(image_path)

# Resize the image to the target size expected by the model (224x224 for VGG16)
img = img.resize((224, 224))

# Convert the image to an array
img_array = image.img_to_array(img)

# Add batch dimension
img_array = np.expand_dims(img_array, axis=0)

# Preprocess the image (using VGG16 preprocess function)
img_array = preprocess_input(img_array)

# Save the processed image (optional)
save_image(img_array[0], os.path.basename(image_path))

# Save only the first batch item
return img_array

def load_and_preprocess_image(image_path): """ Load and preprocess an image for model prediction. """
img_array = preprocess_image(image_path)

return img_array

# Additional image processing functions can be added here
def resize_image(image_path, target_size=(224, 224)): """ Resize an image to the target size. """
img = Image.open(image_path)
img = img.resize(target_size)
return img

def convert_to_grayscale(image_path):""" Convert an image to grayscale. """
img = Image.open(image_path).convert('L')

# 'L' mode is for grayscale return img
def rotate_image(image_path, angle): """ Rotate an image by the specified angle. """
img = Image.open(image_path)
img = img.rotate(angle)
return img

def apply_filter(image_path, filter_type): """ Apply a specified filter to an image. """
img = Image.open(image_path)

if filter_type == 'blur':
    from PIL import ImageFilter
img = img.filter(ImageFilter.BLUR)
elif filter_type == 'sharpen': from PIL import ImageFilter
img = img.filter(ImageFilter.SHARPEN)

return img

if __name__ == "__main__": # Example usage
example_image_path = "path_to_your_image.jpg"
processed_image = load_and_preprocess_image(example_image_path)
print("Image processed and ready for prediction.")