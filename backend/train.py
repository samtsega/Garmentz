import numpy as np
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.optimizers import Adam
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

# Image Data Generators for training and validation
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255, # Normalize pixel values to [0, 1]
    shear_range=0.2, # Randomly shear images
    zoom_range=0.2, # Randomly zoom images
    horizontal_flip=True, # Randomly flip images horizontally
    validation_split=0.2 # Reserve 20% of data for validation
)

train_generator = train_datagen.flow_from_directory( 'path_to_wear_tear_dataset/heavily_worn',
    target_size=(224, 224), # Resize images batch_size=32,
    class_mode='categorical',
    subset='training' # Subset for training
)

validation_generator = train_datagen.flow_from_directory( 'path_to_wear_tear_dataset/heavily_worn',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation' # Subset for validation
)

# Model architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(train_generator.num_classes, activation='softmax') # Softmax for multi-class classification
])

# Compile the model
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
model.fit(
    train_generator,

steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_data=validation_generator,
validation_steps=validation_generator.samples // validation_generator.batch_size,
    epochs=10 # Adjust based on dataset size
)

# Save the trained model to an H5 file

model.save('wear_and_tear_model.h5')