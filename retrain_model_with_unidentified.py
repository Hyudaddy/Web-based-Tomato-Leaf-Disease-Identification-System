#!/usr/bin/env python3
"""
Retrain the model with the new Unidentified class
This is a fine-tuning process - we load the existing model and train for just 5-10 epochs
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

# Dataset paths
DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")
VAL_PATH = os.path.join(DATASET_PATH, "validation")
EXISTING_MODEL_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito.h5"
NEW_MODEL_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito_v2.h5"

# Hyperparameters
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 8  # Fine-tuning - just 8 epochs
LEARNING_RATE = 0.0001  # Lower learning rate for fine-tuning

print("=" * 60)
print("RETRAINING MODEL WITH UNIDENTIFIED CLASS")
print("=" * 60)

# Data augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Only rescaling for validation
val_datagen = ImageDataGenerator(rescale=1./255)

# Load training data
print("\nLoading training data...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Load validation data
print("Loading validation data...")
val_generator = val_datagen.flow_from_directory(
    VAL_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

print(f"\nTraining samples: {train_generator.samples}")
print(f"Validation samples: {val_generator.samples}")
print(f"Number of classes: {train_generator.num_classes}")
print(f"Class labels: {train_generator.class_indices}")

# Load existing model
print("\n" + "=" * 60)
print("Loading existing model for fine-tuning...")
print("=" * 60)

try:
    existing_model = tf.keras.models.load_model(EXISTING_MODEL_PATH)
    print(f"✓ Existing model loaded from: {EXISTING_MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading existing model: {e}")
    raise

# Get the base model (everything except the last layer)
# The existing model has: MobileNetV2 -> GlobalAveragePooling2D -> Dense(256) -> Dense(10)
# We need to rebuild it with 11 classes (10 diseases + 1 unidentified)

print("\n" + "=" * 60)
print("Rebuilding model with new Unidentified class...")
print("=" * 60)

# Extract the base model (MobileNetV2)
base_model = existing_model.layers[1]  # The MobileNetV2 layer

# Freeze base model layers (we only want to train the top layers)
base_model.trainable = False

# Build new model with 11 classes
inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base_model(inputs, training=False)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)
outputs = Dense(train_generator.num_classes, activation='softmax')(x)

new_model = Model(inputs, outputs)

# Compile model with lower learning rate for fine-tuning
new_model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\nNew Model Summary:")
new_model.summary()

# Train model
print("\n" + "=" * 60)
print("Starting fine-tuning training...")
print("=" * 60)

history = new_model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    verbose=1
)

# Evaluate on validation set
print("\n" + "=" * 60)
print("Evaluating model...")
print("=" * 60)

val_loss, val_accuracy = new_model.evaluate(val_generator)
print(f"\nValidation Loss: {val_loss:.4f}")
print(f"Validation Accuracy: {val_accuracy:.4f}")

# Save new model
print(f"\nSaving new model to: {NEW_MODEL_PATH}")
new_model.save(NEW_MODEL_PATH)
print("✓ New model saved successfully!")

print("\n" + "=" * 60)
print("RETRAINING COMPLETE!")
print("=" * 60)
print(f"\n📝 NEXT STEPS:")
print(f"1. Backup your current model:")
print(f"   - Copy: {EXISTING_MODEL_PATH}")
print(f"   - To: {EXISTING_MODEL_PATH}.backup")
print(f"\n2. Replace the old model with the new one:")
print(f"   - Copy: {NEW_MODEL_PATH}")
print(f"   - To: {EXISTING_MODEL_PATH}")
print(f"\n3. Restart your backend API")
print(f"4. Test with non-tomato images!")
print("\n✅ The model now has 11 classes:")
for i, (class_name, idx) in enumerate(sorted(train_generator.class_indices.items(), key=lambda x: x[1])):
    print(f"   {idx}: {class_name}")
