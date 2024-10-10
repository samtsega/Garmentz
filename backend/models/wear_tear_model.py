import os
import numpy as np
import tf_keras
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Flatten, Dropout
from tf_keras.applications import VGG16
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.optimizers import Adam

# Ensure the TensorFlow version is correct
print(f"Using TensorFlow version: {tf_keras.__version__}")

# 1. Load the pretrained VGG16 model, excluding the top layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# 2. Freeze the base model to prevent its weights from updating during training
base_model.trainable = False

# 3. Create a new model and add custom layers on top of the pretrained model
model = Sequential([
    base_model,              # Add the VGG16 base model
    Flatten(),               # Flatten the output to feed into fully connected layers
    Dense(256, activation='relu'),  # Dense layer with 256 units and ReLU activation
    Dropout(0.5),            # Dropout layer to reduce overfitting
    Dense(128, activation='relu'),  # Another dense layer
    Dense(1, activation='sigmoid')   # Output layer for wear and tear score (0 to 1)
])

# 4. Compile the model with Adam optimizer and binary crossentropy for the loss
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['mae'])

# 5. Set up ImageDataGenerator for loading and augmenting the images
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,        # Normalize pixel values
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1.0 / 255)  # Only normalize validation data

# 6. Load the training and validation data from directories
train_generator = train_datagen.flow_from_directory(
    'path_to_your_dataset/train',          # Update with actual dataset path
    target_size=(224, 224),                # Match the input size expected by VGG16
    batch_size=32,
    class_mode='binary'                     # 'binary' for wear and tear score (0 or 1)
)

validation_generator = val_datagen.flow_from_directory(
    'path_to_your_dataset/validation',     # Update with actual dataset path
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'                     # 'binary' for wear and tear score
)

# 7. Train the model
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    epochs=10  # Adjust epochs based on your needs
)

# 8. Save the trained model to an .h5 file
model.save('wear_and_tear_model.h5')
print("Model saved as wear_and_tear_model.h5")

# Function to predict wear and tear score for a new image
def predict_wear_and_tear(image_path):
    """Predict wear and tear score for a given image."""
    img = tf_keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf_keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize pixel values

    score = model.predict(img_array)  # Get the wear and tear score
    return score[0][0]  # Return the score
