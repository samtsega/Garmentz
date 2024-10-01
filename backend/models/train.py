from tf_keras.applications import VGG16
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Flatten, Dropout
from tf_keras.preprocessing.image import ImageDataGenerator
from tf_keras.optimizers import Adam

# Load VGG16, without the top layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False

# Add custom layers
model = Sequential([
    base_model,
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5), Dense(128, activation='relu'),
    Dense(3, activation='softmax') # Adjust this according to your number of classes
    ])

# Compile the model model.
compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Data generators for loading images
train_datagen = ImageDataGenerator(rescale=1.0/255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
val_datagen = ImageDataGenerator(rescale=1.0/255)

train_generator = train_datagen.flow_from_directory('datasets/train', target_size=(224, 224), batch_size=32, class_mode='categorical')
validation_generator = val_datagen.flow_from_directory('datasets/validation', target_size=(224, 224), batch_size=32, class_mode='categorical')

# Train the model
model.fit(train_generator, steps_per_epoch=train_generator.samples // train_generator.batch_size, validation_data=validation_generator, validation_steps=validation_generator.samples // validation_generator.batch_size, epochs=5)

# Save the model

model.save('models/depreciation_model.h5')