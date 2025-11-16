#!/usr/bin/env python3
"""
Optimized training script for full dataset with better accuracy on low-quality images
Option C: Balanced approach - 192x192 images, good augmentation, 35 epochs with early stopping
Optimized for CPU training (Intel Core i3)
"""

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

# Dataset paths
DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")
VAL_PATH = os.path.join(DATASET_PATH, "validation")
MODEL_SAVE_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito.h5"
BACKUP_MODEL_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito_backup.h5"
HISTORY_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\training_history.json"

# Optimized hyperparameters for CPU (Option C - Balanced)
IMG_SIZE = 192  # Balanced: not too large for CPU, good for feature extraction
BATCH_SIZE = 20  # Reduced from 32 for CPU efficiency and better gradient updates
EPOCHS = 35  # Increased from 20 for better training
LEARNING_RATE = 0.0005  # Reduced from 0.001 for more careful learning
VALIDATION_SPLIT = 0.2

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

# Enhanced data augmentation for low-quality images
# This helps the model learn to recognize diseases even in poor lighting/quality
train_datagen = ImageDataGenerator(
    rescale=1./255,
    # Rotation and shift
    rotation_range=25,  # Increased from 20
    width_shift_range=0.25,  # Increased from 0.2
    height_shift_range=0.25,  # Increased from 0.2
    shear_range=0.25,  # Increased from 0.2
    zoom_range=0.25,  # Increased from 0.2
    # NEW: Brightness and contrast adjustments for low-quality images
    brightness_range=[0.7, 1.3],  # Handle dim/bright images
    # Flips
    horizontal_flip=True,
    vertical_flip=True,  # NEW: Additional flip for leaf orientation
    fill_mode='nearest'
)

# Only rescaling for validation (no augmentation)
val_datagen = ImageDataGenerator(rescale=1./255)

# Load training data
print("\n" + "=" * 80)
print("Loading training data...")
print("=" * 80)
try:
    train_generator = train_datagen.flow_from_directory(
        TRAIN_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    print(f"✓ Training data loaded successfully")
except Exception as e:
    print(f"❌ Error loading training data: {e}")
    print(f"Please ensure training data exists at: {TRAIN_PATH}")
    raise

# Load validation data
print("Loading validation data...")
try:
    val_generator = val_datagen.flow_from_directory(
        VAL_PATH,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
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

# Build model using transfer learning
print("\n" + "=" * 80)
print("Building model with MobileNetV2 transfer learning...")
print("=" * 80)

# Load pre-trained MobileNetV2
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze base model layers for transfer learning
base_model.trainable = False

# Add custom top layers with improved architecture
inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base_model(inputs, training=False)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)  # Increased from 0.2
x = Dense(512, activation='relu')(x)  # Increased from 256
x = Dropout(0.3)(x)  # Increased from 0.2
x = Dense(256, activation='relu')(x)  # NEW: Additional dense layer
x = Dropout(0.2)(x)
outputs = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs, outputs)

# Compile model
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n📐 Model Summary:")
model.summary()

# Callbacks for better training
callbacks = [
    # Save best model during training
    ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    ),
    # Early stopping to prevent overfitting
    EarlyStopping(
        monitor='val_loss',
        patience=5,  # Stop if no improvement for 5 epochs
        restore_best_weights=True,
        verbose=1
    ),
    # Reduce learning rate if validation loss plateaus
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
]

# Train model
print("\n" + "=" * 80)
print("Starting training with full dataset...")
print("=" * 80)
print("⏳ This may take 30-60 minutes on CPU. Please be patient...\n")

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    callbacks=callbacks,
    verbose=1
)

# Evaluate on validation set
print("\n" + "=" * 80)
print("Evaluating model on validation set...")
print("=" * 80)

val_loss, val_accuracy = model.evaluate(val_generator)
print(f"\n✅ Validation Loss: {val_loss:.4f}")
print(f"✅ Validation Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")

# Save training history
print(f"\nSaving training history...")
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
