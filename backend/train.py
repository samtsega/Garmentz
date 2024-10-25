from tf_keras.models import Sequential
from tf_keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tf_keras.preprocessing.image import ImageDataGenerator
import os

# Set up paths and constants
train_data_dir = './data/train'  # Path to training data
validation_data_dir = './data/validation'  # Path to validation data
img_width, img_height = 150, 150  # Image dimensions (can adjust based on your dataset)
batch_size = 32
epochs = 10
num_classes = 5  # Adjust based on the number of categories (e.g., clothing types)
model_save_path = 'clothing_model.h5'

# Preprocessing: Set up ImageDataGenerator for training and validation
train_datagen = ImageDataGenerator(
    rescale=1.0/255,  # Normalize pixel values
    shear_range=0.2,  # Randomly shear images
    zoom_range=0.2,   # Randomly zoom images
    horizontal_flip=True  # Randomly flip images horizontally
)

validation_datagen = ImageDataGenerator(rescale=1.0/255)  # Only rescale validation data

# Load the training data
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'  # Use 'categorical' for multi-class classification
)

# Load the validation data
validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

# Define the CNN model
model = Sequential()

# Add layers to the model
model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flatten the results to feed into a dense layer
model.add(Flatten())

# Add a fully connected layer
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))  # Dropout to prevent overfitting
model.add(Dense(num_classes, activation='softmax'))  # Output layer (adjust for the number of categories)

# Compile the model
model.compile(
    loss='categorical_crossentropy',  # Use categorical cross-entropy for multi-class classification
    optimizer='adam',  # Adam optimizer
    metrics=['accuracy']  # Track accuracy during training
)

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# Save the model
model.save(model_save_path)
print(f"Model saved to {model_save_path}")

