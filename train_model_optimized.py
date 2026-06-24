#!/usr/bin/env python3
"""
================================================================================
FITO - TOMATO LEAF DISEASE DETECTION MODEL TRAINING SCRIPT
================================================================================

This script handles the complete training pipeline for the disease classification model.

TRAINING PROCESS FLOW:
----------------------
1. CONFIGURATION     - Set hyperparameters (epochs, batch size, learning rate)
2. DATA PREPARATION  - Load and augment training/validation images
3. MODEL BUILDING    - Create neural network using transfer learning (MobileNetV2)
4. TRAINING          - Train the model on the dataset
5. VALIDATION        - Evaluate model performance on unseen data
6. SAVING            - Save trained model and training history

Optimized for CPU training (Intel Core i3)
"""

# ================================================================================
# IMPORTS - Required libraries for deep learning and data processing
# ================================================================================
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import os
import json
from datetime import datetime

# ================================================================================
# STEP 1: CONFIGURATION - Define paths and hyperparameters
# ================================================================================
# This is where we configure all the settings BEFORE training begins.
# The hyperparameters control HOW the model learns.

# Dataset paths - Where the images are stored
DATASET_PATH = r"C:\Users\altai\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")     # Training images (80%)
VAL_PATH = os.path.join(DATASET_PATH, "validation")     # Validation images (20%)
MODEL_SAVE_PATH = r"C:\Users\altai\Desktop\TLDI_system\backend\trained_model_fito.h5"
BACKUP_MODEL_PATH = r"C:\Users\altai\Desktop\TLDI_system\backend\trained_model_fito_backup.h5"
HISTORY_PATH = r"C:\Users\altai\Desktop\TLDI_system\training_history.json"

# HYPERPARAMETERS - These control how the model learns
# -------------------------------------------------------------------
IMG_SIZE = 192      # Image resolution: 192x192 pixels (input size to model)
BATCH_SIZE = 20     # Number of images processed together in one step
EPOCHS = 35         # Number of complete passes through the entire dataset
LEARNING_RATE = 0.0005  # How fast the model adjusts weights (lower = more careful)
VALIDATION_SPLIT = 0.2  # 20% of data used for validation

print("=" * 80)
print("TOMATO LEAF DISEASE DETECTION - OPTIMIZED FULL DATASET TRAINING")
print("=" * 80)
print(f"\n📋 Training Configuration (Option C - Balanced for CPU):")
print(f"   • Image Size: {IMG_SIZE}x{IMG_SIZE}")
print(f"   • Batch Size: {BATCH_SIZE}")
print(f"   • Epochs: {EPOCHS} (with early stopping)")
print(f"   • Learning Rate: {LEARNING_RATE}")
print(f"   • Device: CPU (Intel Core i3)")
print(f"   • Dataset Path: {DATASET_PATH}")
print(f"\n⏱️  Estimated training time: 30-60 minutes (depending on dataset size)")

# ================================================================================
# STEP 2: DATA PREPARATION - Configure how images are loaded and augmented
# ================================================================================
# Data augmentation artificially increases dataset variety by creating modified
# versions of images (rotated, flipped, brightness adjusted). This helps the
# model generalize better to real-world images with different lighting/angles.

# TRAINING DATA AUGMENTATION - Apply transformations to increase variety
train_datagen = ImageDataGenerator(
    rescale=1./255,             # Normalize pixel values from 0-255 to 0-1
    rotation_range=25,          # Rotate images randomly up to 25 degrees
    width_shift_range=0.25,     # Shift image horizontally by up to 25%
    height_shift_range=0.25,    # Shift image vertically by up to 25%
    shear_range=0.25,           # Apply shearing transformation
    zoom_range=0.25,            # Zoom in/out by up to 25%
    brightness_range=[0.7, 1.3],  # Adjust brightness (for poor lighting)
    horizontal_flip=True,       # Flip images horizontally
    vertical_flip=True,         # Flip images vertically
    fill_mode='nearest'         # How to fill empty pixels after transforms
)

# VALIDATION DATA - Only normalize, NO augmentation (to test on real data)
val_datagen = ImageDataGenerator(rescale=1./255)

# LOAD TRAINING DATA - Read images from the training folder
# The generator reads images from folders, where each folder name = class label
print("\n" + "=" * 80)
print("STEP 2A: Loading training data...")
print("=" * 80)
try:
    train_generator = train_datagen.flow_from_directory(
        TRAIN_PATH,                         # Path to training images folder
        target_size=(IMG_SIZE, IMG_SIZE),   # Resize all images to 192x192
        batch_size=BATCH_SIZE,              # Load 20 images at a time
        class_mode='categorical',           # Multi-class classification (one-hot)
        shuffle=True                        # Randomize order each epoch
    )
    print(f"✓ Training data loaded successfully")
except Exception as e:
    print(f"❌ Error loading training data: {e}")
    print(f"Please ensure training data exists at: {TRAIN_PATH}")
    raise

# LOAD VALIDATION DATA - Used to check model performance during training
print("STEP 2B: Loading validation data...")
try:
    val_generator = val_datagen.flow_from_directory(
        VAL_PATH,                           # Path to validation images folder
        target_size=(IMG_SIZE, IMG_SIZE),   # Same size as training
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False                       # Don't shuffle for consistent evaluation
    )
    print(f"✓ Validation data loaded successfully")
except Exception as e:
    print(f"❌ Error loading validation data: {e}")
    print(f"Please ensure validation data exists at: {VAL_PATH}")
    raise

print(f"\n📊 Dataset Summary:")
print(f"   • Training samples: {train_generator.samples}")
print(f"   • Validation samples: {val_generator.samples}")
print(f"   • Number of classes: {train_generator.num_classes}")
print(f"   • Classes: {list(train_generator.class_indices.keys())}")

# ================================================================================
# STEP 3: MODEL BUILDING - Create the neural network architecture
# ================================================================================
# We use TRANSFER LEARNING: start with a pre-trained model (MobileNetV2)
# that already knows how to extract image features, then add our own
# classification layers on top for tomato disease detection.

print("\n" + "=" * 80)
print("STEP 3: Building model with MobileNetV2 transfer learning...")
print("=" * 80)

# STEP 3A: Load pre-trained MobileNetV2 (trained on ImageNet - 1M+ images)
# This model already knows how to recognize patterns, edges, textures, etc.
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),  # 192x192 RGB images
    include_top=False,                     # Remove original classification layer
    weights='imagenet'                     # Use pre-trained ImageNet weights
)

# STEP 3B: Freeze base model - Don't retrain the pre-trained layers
# We only want to train our custom layers on top
base_model.trainable = False

# STEP 3C: Add custom classification layers for tomato disease detection
# This is where we customize for our specific 11-class problem
inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base_model(inputs, training=False)    # Pass through MobileNetV2
x = GlobalAveragePooling2D()(x)           # Reduce feature maps to 1D
x = Dropout(0.3)(x)                       # Dropout: randomly disable 30% of neurons (prevents overfitting)
x = Dense(512, activation='relu')(x)      # Fully connected layer: 512 neurons
x = Dropout(0.3)(x)                       # More dropout
x = Dense(256, activation='relu')(x)      # Fully connected layer: 256 neurons
x = Dropout(0.2)(x)
outputs = Dense(train_generator.num_classes, activation='softmax')(x)  # Output: 11 classes

model = Model(inputs, outputs)

# STEP 3D: Compile model - Define how it learns
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),  # Optimizer: how weights are updated
    loss='categorical_crossentropy',               # Loss function for multi-class
    metrics=['accuracy']                           # Track accuracy during training
)

print("\n📐 Model Summary:")
model.summary()

# ================================================================================
# STEP 4: TRAINING - Train the model on the dataset
# ================================================================================
# This is the main training loop where the model learns from the images.
# For each epoch, the model sees ALL training images and adjusts its weights.

# CALLBACKS - Special functions that run during training
callbacks = [
    # ModelCheckpoint: Save the model whenever validation accuracy improves
    ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_accuracy',    # Watch validation accuracy
        save_best_only=True,       # Only save if it's the best so far
        mode='max',
        verbose=1
    ),
    # EarlyStopping: Stop training if model stops improving (prevents overfitting)
    EarlyStopping(
        monitor='val_loss',
        patience=5,                # Stop if no improvement for 5 epochs
        restore_best_weights=True, # Go back to the best weights
        verbose=1
    ),
    # ReduceLROnPlateau: Lower learning rate if training plateaus
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,                # Reduce LR by half
        patience=3,                # Wait 3 epochs before reducing
        min_lr=1e-7,
        verbose=1
    )
]

# *** THIS IS WHERE THE ACTUAL TRAINING HAPPENS ***
print("\n" + "=" * 80)
print("STEP 4: Starting training with full dataset...")
print("=" * 80)
print("⏳ This may take 30-60 minutes on CPU. Please be patient...\n")

# model.fit() - THE MAIN TRAINING FUNCTION
# Each epoch: model processes all 20,452 training images in batches of 20
# After each epoch: evaluate on 5,488 validation images to track progress
history = model.fit(
    train_generator,              # Training data
    epochs=EPOCHS,                # Train for 35 epochs (or until early stop)
    validation_data=val_generator,  # Validation data to monitor overfitting
    callbacks=callbacks,          # Run checkpoint, early stop, LR reduction
    verbose=1                     # Show progress bar
)

# ================================================================================
# STEP 5: VALIDATION/TESTING - Evaluate the trained model
# ================================================================================
# After training, we evaluate the model on the validation set one final time
# to get the official accuracy metrics.

print("\n" + "=" * 80)
print("STEP 5: Evaluating model on validation set...")
print("=" * 80)

# Evaluate the model on validation data (5,488 images it hasn't trained on)
val_loss, val_accuracy = model.evaluate(val_generator)
print(f"\n✅ Validation Loss: {val_loss:.4f}")
print(f"✅ Validation Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")

# ================================================================================
# STEP 6: SAVING - Save the trained model and training history
# ================================================================================
# Save the model file (.h5) and training metrics for later analysis.
# The model file is what gets loaded by the backend API for predictions.

print(f"\nSTEP 6: Saving training history...")
history_dict = {
    'accuracy': [float(x) for x in history.history['accuracy']],
    'loss': [float(x) for x in history.history['loss']],
    'val_accuracy': [float(x) for x in history.history['val_accuracy']],
    'val_loss': [float(x) for x in history.history['val_loss']],
    'final_val_accuracy': float(val_accuracy),
    'final_val_loss': float(val_loss),
    'timestamp': datetime.now().isoformat(),
    'config': {
        'img_size': IMG_SIZE,
        'batch_size': BATCH_SIZE,
        'epochs': EPOCHS,
        'learning_rate': LEARNING_RATE,
        'training_samples': train_generator.samples,
        'validation_samples': val_generator.samples,
        'num_classes': train_generator.num_classes,
        'classes': list(train_generator.class_indices.keys())
    }
}

with open(HISTORY_PATH, 'w') as f:
    json.dump(history_dict, f, indent=2)
print(f"✓ History saved to: {HISTORY_PATH}")

print("\n" + "=" * 80)
print("TRAINING COMPLETE!")
print("=" * 80)
print(f"\n✅ New model saved at: {MODEL_SAVE_PATH}")
print(f"\n📊 Training Results:")
print(f"   • Final Validation Accuracy: {val_accuracy:.2%}")
print(f"   • Final Validation Loss: {val_loss:.4f}")
print(f"   • Total Epochs Trained: {len(history.history['accuracy'])}")

print(f"\n📝 NEXT STEPS:")
print(f"   1. Backup your current model:")
print(f"      - Copy: {r'C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito.h5'}")
print(f"      - To: {BACKUP_MODEL_PATH}")
print(f"\n   2. The new model is already saved at:")
print(f"      - {MODEL_SAVE_PATH}")
print(f"\n   3. Restart your backend API to load the new model")
print(f"\n   4. Test with low-quality tomato leaf images")
print(f"\n   5. Check training history at: {HISTORY_PATH}")

print(f"\n💡 Key Improvements in this training:")
print(f"   ✓ Enhanced data augmentation for low-quality images")
print(f"   ✓ Brightness/contrast adjustments for poor lighting")
print(f"   ✓ Larger image size (192x192) for better feature extraction")
print(f"   ✓ Smaller batch size (20) for better gradient updates on CPU")
print(f"   ✓ Lower learning rate (0.0005) for more careful learning")
print(f"   ✓ Early stopping to prevent overfitting")
print(f"   ✓ Learning rate reduction on plateau")

print(f"\n🎯 Expected Improvements:")
print(f"   • Better accuracy on low-quality images")
print(f"   • Better handling of poor lighting conditions")
print(f"   • More robust disease detection")
print(f"   • Fewer 'cannot identify' results")

print("\n" + "=" * 80)
