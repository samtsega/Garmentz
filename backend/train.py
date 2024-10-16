import numpy as np
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.optimizers import Adam
import os
import tensorflow as tf

# Paths
dataset_dir = 'path/to/your/dataset'  # Replace with the path to your dataset
model_save_path = 'models/depreciation_model.h5'

# Parameters
img_width, img_height = 224, 224
batch_size = 32
epochs = 10  # Adjust based on your needs
num_classes = 3  # For 'heavily lightly_worn', 'lightly lightly_worn', and 'not lightly_worn'

# Data Augmentation and Preprocessing
datagen = ImageDataGenerator(
    rescale=1.0 / 255,        # Normalize pixel values to [0, 1]
    shear_range=0.2,          # Apply random shear transformations
    zoom_range=0.2,           # Randomly zoom into images
    horizontal_flip=True,     # Randomly flip images horizontally
    validation_split=0.2      # Split data into 80% training, 20% validation
)

# Load the training and validation data
train_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',  # Multi-class classification
    subset='training'         # Training data
)

validation_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',  # Multi-class classification
    subset='validation'       # Validation data
)

# Build the Model using MobileNetV2 (Transfer Learning)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))

# Freeze the base model layers
base_model.trainable = False

# Add custom layers on top of the base model
x = base_model.output
x = GlobalAveragePooling2D()(x)  # Global average pooling layer
x = Dense(1024, activation='relu')(x)  # Fully connected layer with 1024 units
output = Dense(num_classes, activation='softmax')(x)  # Output layer with 3 classes

# Create the final model
model = Model(inputs=base_model.input, outputs=output)

# Compile the model
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    validation_steps=validation_generator.samples // batch_size,
    validation_data=validation_generator,
    epochs=epochs
)

# Save the trained model
if not os.path.exists('models'):
    os.makedirs('models')
model.save(model_save_path)

print(f"Model saved to {model_save_path}")
