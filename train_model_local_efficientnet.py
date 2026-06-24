#!/usr/bin/env python3
"""
================================================================================
FITO - TOMATO LEAF DISEASE DETECTION MODEL TRAINING SCRIPT
================================================================================
Local Training Version with EfficientNetB0 (224x224) for Higher Accuracy

OPTIMIZED FOR:
--------------
- Intel Core i3-6006U @ 2.00GHz (2 cores, 4 threads)
- 12 GB RAM
- CPU-only training (no dedicated GPU)

ESTIMATED TRAINING TIME: 4-6 hours (50 epochs)

TRAINING PROCESS FLOW:
----------------------
1. CONFIGURATION   - Set hyperparameters (epochs, batch size, learning rate)
2. DATA PREPARATION- Load and augment training/validation images
3. MODEL BUILDING  - Create neural network using transfer learning (EfficientNetB0)
4. TRAINING        - Train the model on the dataset
5. VALIDATION      - Evaluate model performance on unseen data
6. SAVING          - Save trained model and training history

HOW TO RUN:
-----------
1. Open terminal in the TLDI_system folder
2. Run: python train_model_local_efficientnet.py
3. Wait for training to complete (4-6 hours)
4. The new model will be saved as: trained_model_efficientnet.h5
"""

# ================================================================================
# IMPORTS - Required libraries for deep learning and data processing
# ================================================================================
print("=" * 80)
print("FITO - EfficientNetB0 LOCAL TRAINING")
print("Optimized for Intel Core i3-6006U with 12GB RAM")
print("=" * 80)
print("\nLoading libraries (this may take a moment)...")

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import os
import json
from datetime import datetime

print("✓ All libraries loaded successfully!")
print(f"TensorFlow version: {tf.__version__}")

# Check for GPU (you have integrated Intel HD Graphics - won't help much)
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"GPU detected: {gpus}")
else:
    print("No dedicated GPU - using CPU for training")
    print("This will take longer but will work fine!")

# ================================================================================
# STEP 1: CONFIGURATION - Define paths and hyperparameters
# ================================================================================
# This is where we configure all the settings BEFORE training begins.
# The hyperparameters are OPTIMIZED for your Intel i3 processor.

print("\n" + "=" * 80)
print("STEP 1: CONFIGURATION - Setting Hyperparameters")
print("=" * 80)

# Dataset paths - YOUR LOCAL PATHS
DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")      # Training images
VAL_PATH = os.path.join(DATASET_PATH, "validation")      # Validation images

# Output paths - Where to save the trained model
MODEL_SAVE_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\trained_model_efficientnet.h5"
BACKUP_MODEL_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\trained_model_efficientnet_backup.h5"
HISTORY_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\training_history_efficientnet.json"

# HYPERPARAMETERS - OPTIMIZED FOR YOUR i3 PROCESSOR + 12GB RAM
# ==============================================================================
IMG_SIZE = 224          # Image resolution: 224x224 (optimal for EfficientNet)
BATCH_SIZE = 12         # Balanced for RAM efficiency and training speed
EPOCHS = 50             # Number of training cycles
LEARNING_RATE = 0.001   # How fast the model adjusts weights

# Display configuration
print(f"""
📋 Training Configuration (EfficientNetB0 for i3 CPU):
   • Model: EfficientNetB0 (pre-trained on ImageNet)
   • Image Size: {IMG_SIZE}x{IMG_SIZE} pixels (higher detail)
   • Batch Size: {BATCH_SIZE} images per step (optimized for 12GB RAM)
   • Epochs: {EPOCHS} training cycles
   • Learning Rate: {LEARNING_RATE}
   • Device: Intel Core i3-6006U CPU
   
📁 Dataset Paths:
   • Training: {TRAIN_PATH}
   • Validation: {VAL_PATH}
   
💾 Output:
   • Model will be saved to: {MODEL_SAVE_PATH}
   
⏱️ Estimated Training Time: 4-6 hours
   (You can leave this running in the background)
""")

# Verify dataset exists
if not os.path.exists(TRAIN_PATH):
    print(f"❌ ERROR: Training folder not found at: {TRAIN_PATH}")
    exit(1)
else:
    print(f"✓ Training folder found!")
    
if not os.path.exists(VAL_PATH):
    print(f"❌ ERROR: Validation folder not found at: {VAL_PATH}")
    exit(1)
else:
    print(f"✓ Validation folder found!")

# ================================================================================
# STEP 2: DATA PREPARATION - Configure how images are loaded and augmented
# ================================================================================
# Data augmentation artificially increases dataset variety by creating modified
# versions of images (rotated, flipped, brightness adjusted). This helps the
# model generalize better to real-world images with different lighting/angles.

print("\n" + "=" * 80)
print("STEP 2: DATA PREPARATION - Loading and Augmenting Images")
print("=" * 80)

# TRAINING DATA AUGMENTATION - Apply transformations to increase variety
# These transformations create variations of your images to help the model
# learn to recognize diseases from different angles, lighting conditions, etc.
train_datagen = ImageDataGenerator(
    rescale=1./255,             # Normalize pixel values from 0-255 to 0-1
    rotation_range=30,          # Rotate images randomly up to 30 degrees
    width_shift_range=0.2,      # Shift image horizontally by up to 20%
    height_shift_range=0.2,     # Shift image vertically by up to 20%
    shear_range=0.2,            # Apply shearing transformation
    zoom_range=0.2,             # Zoom in/out by up to 20%
    brightness_range=[0.8, 1.2],  # Adjust brightness (for poor lighting)
    horizontal_flip=True,       # Flip images horizontally
    vertical_flip=True,         # Flip images vertically
    fill_mode='nearest'         # How to fill empty pixels after transforms
)

# VALIDATION DATA - Only normalize, NO augmentation
# Validation data should represent real-world images without modifications
val_datagen = ImageDataGenerator(rescale=1./255)

# LOAD TRAINING DATA - Read images from the training folder
# The generator reads images from folders, where each folder name = class label
print("Loading training data (this may take a minute)...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_PATH,                         # Path to training images folder
    target_size=(IMG_SIZE, IMG_SIZE),   # Resize all images to 224x224
    batch_size=BATCH_SIZE,              # Load 8 images at a time (RAM optimized)
    class_mode='categorical',           # Multi-class classification (one-hot)
    shuffle=True                        # Randomize order each epoch
)
print(f"✓ Training data loaded: {train_generator.samples} images")

# LOAD VALIDATION DATA - Used to check model performance during training
print("Loading validation data...")
val_generator = val_datagen.flow_from_directory(
    VAL_PATH,                           # Path to validation images folder
    target_size=(IMG_SIZE, IMG_SIZE),   # Same size as training
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False                       # Don't shuffle for consistent evaluation
)
print(f"✓ Validation data loaded: {val_generator.samples} images")

# Display dataset summary
print(f"""
📊 Dataset Summary:
   • Training samples: {train_generator.samples}
   • Validation samples: {val_generator.samples}
   • Number of classes: {train_generator.num_classes}
   • Classes: {list(train_generator.class_indices.keys())}
   • Steps per epoch: {train_generator.samples // BATCH_SIZE}
""")

# ================================================================================
# STEP 3: MODEL BUILDING - Create the neural network architecture
# ================================================================================
# We use TRANSFER LEARNING: start with a pre-trained model (EfficientNetB0)
# that already knows how to extract image features, then add our own
# classification layers on top for tomato disease detection.
#
# WHY EfficientNetB0?
# -------------------
# - More accurate than MobileNetV2 (typically 2-5% higher accuracy)
# - Efficient architecture with compound scaling
# - Pre-trained on ImageNet (1.4M images, 1000 classes)
# - 224x224 input captures more detail than 192x192

print("\n" + "=" * 80)
print("STEP 3: MODEL BUILDING - Creating EfficientNetB0 Architecture")
print("=" * 80)

# STEP 3A: Build model using transfer learning
# Fix for Keras 3 shape mismatch: Build without weights, then load manually
tf.keras.backend.clear_session()

print("Building EfficientNetB0 model...")

# Create the input tensor explicitly first
inputs = tf.keras.Input(shape=(224, 224, 3))

# Load base model structure WITHOUT weights to avoid shape mismatch
# This ensures the model is built with the correct 3-channel architecture
base_model = EfficientNetB0(
    weights=None,  # Do not load weights during instantiation
    include_top=False,
    input_tensor=inputs
)
base_model.trainable = False

print(f"✓ EfficientNetB0 architecture created with {len(base_model.layers)} layers")

# Manually load ImageNet weights
print("Downloading and loading ImageNet weights...")
weights_path = tf.keras.utils.get_file(
    'efficientnetb0_notop.h5',
    'https://storage.googleapis.com/keras-applications/efficientnetb0_notop.h5',
    cache_subdir='models',
    file_hash='1618d38a71981e47de93a3f3579981d9'
)
base_model.load_weights(weights_path)
print("✓ ImageNet weights loaded successfully!")

# STEP 3B: Connect custom layers
# inputs is already defined above
x = base_model(inputs, training=False)
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dropout(0.4)(x)
x = Dense(512, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.3)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)
outputs = Dense(train_generator.num_classes, activation='softmax')(x)

# Create the final model
model = Model(inputs, outputs)

# STEP 3D: Compile model - Define how it learns
print("Compiling model...")
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),  # Adam optimizer
    loss='categorical_crossentropy',               # Loss for multi-class
    metrics=['accuracy']                           # Track accuracy
)

print("\n📐 Model Architecture Summary:")
model.summary()

total_params = model.count_params()
trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
print(f"""
✓ Model built successfully!
   • Base model: EfficientNetB0 (frozen)
   • Custom layers: GlobalPooling -> Dense(512) -> Dense(256) -> Output({train_generator.num_classes})
   • Total parameters: {total_params:,}
   • Trainable parameters: {trainable_params:,}
""")

# ================================================================================
# STEP 4: TRAINING - Train the model on the dataset
# ================================================================================
# This is the main training loop where the model learns from the images.
# For each epoch, the model sees ALL training images and adjusts its weights.
#
# TRAINING METRICS:
# - loss: How wrong the model's predictions are (lower is better)
# - accuracy: Percentage of correct predictions (higher is better)
# - val_loss: Loss on validation data (monitors overfitting)
# - val_accuracy: Accuracy on validation data (actual performance)

print("\n" + "=" * 80)
print("STEP 4: TRAINING - Starting Model Training")
print("=" * 80)

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
    # EarlyStopping: Stop training if model stops improving
    # This prevents overfitting by stopping when validation loss plateaus
    EarlyStopping(
        monitor='val_loss',
        patience=7,                # Stop if no improvement for 7 epochs
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

steps_per_epoch = train_generator.samples // BATCH_SIZE
validation_steps = val_generator.samples // BATCH_SIZE
estimated_time_per_epoch = (steps_per_epoch * 3) // 60  # rough estimate: ~3 seconds per step

print(f"""
🚀 Starting Training:
   • Epochs: {EPOCHS}
   • Batch size: {BATCH_SIZE}
   • Steps per epoch: {steps_per_epoch}
   • Validation steps: {validation_steps}
   • Early stopping patience: 7 epochs
   
⏱️ Estimated time: ~{estimated_time_per_epoch} minutes per epoch
   Total: approximately {estimated_time_per_epoch * EPOCHS // 60} hours
   
💡 TIP: You can minimize this window and let it run in background.
   The best model is automatically saved whenever accuracy improves.
""")

print("\n" + "-" * 80)
print("TRAINING STARTED - Please wait...")
print("-" * 80 + "\n")

# *** THIS IS WHERE THE ACTUAL TRAINING HAPPENS ***
start_time = datetime.now()

history = model.fit(
    train_generator,              # Training data
    epochs=EPOCHS,                # Train for 50 epochs (or until early stop)
    validation_data=val_generator,  # Validation data to monitor overfitting
    callbacks=callbacks,          # Run checkpoint, early stop, LR reduction
    verbose=1                     # Show progress bar
)

end_time = datetime.now()
training_duration = end_time - start_time

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETED!")
print("=" * 80)
print(f"Total training time: {training_duration}")

# ================================================================================
# STEP 5: VALIDATION/EVALUATION - Evaluate the trained model
# ================================================================================
# After training, we evaluate the model on the validation set one final time

print("\n" + "=" * 80)
print("STEP 5: VALIDATION - Evaluating Model Performance")
print("=" * 80)

val_loss, val_accuracy = model.evaluate(val_generator)

print(f"""
📊 FINAL RESULTS:
   ✅ Validation Loss: {val_loss:.4f}
   ✅ Validation Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)
   
   Epochs trained: {len(history.history['accuracy'])}
   Best validation accuracy: {max(history.history['val_accuracy'])*100:.2f}%
   Training time: {training_duration}
""")


# ================================================================================
# COMPLETE! - Summary and Next Steps
# ================================================================================

print("\n" + "=" * 80)
print("🎉 TRAINING COMPLETE!")
print("=" * 80)

print(f"""
📊 TRAINING SUMMARY:
   • Model: EfficientNetB0 (Transfer Learning from ImageNet)
   • Image Size: {IMG_SIZE}x{IMG_SIZE}
   • Final Accuracy: {val_accuracy*100:.2f}%
   • Best Accuracy: {max(history.history['val_accuracy'])*100:.2f}%
   • Epochs Trained: {len(history.history['accuracy'])} / {EPOCHS}
   • Training Time: {training_duration}

📁 SAVED FILES:
   1. {MODEL_SAVE_PATH}
      - The trained model file
   2. {HISTORY_PATH}
      - Training metrics in JSON format

🔧 TO USE THE NEW MODEL:
   1. Copy the new model to the backend folder:
      
      copy "{MODEL_SAVE_PATH}" "{os.path.dirname(MODEL_SAVE_PATH)}\\backend\\trained_model_fito.h5"
      
   2. IMPORTANT: Update model_handler.py to use 224x224 input size:
      - Change line 49: image = image.resize((224, 224))
      
   3. Restart your backend server

📌 COMPARISON:
   • Previous MobileNetV2 (192x192): ~90% accuracy
   • New EfficientNetB0 (224x224): {val_accuracy*100:.2f}% accuracy
""")

print("\n" + "=" * 80)
print("Training script completed successfully!")
print("=" * 80)
# ================================================================================
# STEP 6: SAVE TRAINING HISTORY - Save metrics for documentation
# ================================================================================

print("\n" + "=" * 80)
print("STEP 6: SAVING - Saving Training History")
print("=" * 80)

# Save training history as JSON
history_dict = {
    'accuracy': [float(x) for x in history.history['accuracy']],
    'loss': [float(x) for x in history.history['loss']],
    'val_accuracy': [float(x) for x in history.history['val_accuracy']],
    'val_loss': [float(x) for x in history.history['val_loss']],
    'final_val_accuracy': float(val_accuracy),
    'final_val_loss': float(val_loss),
    'training_duration': str(training_duration),
    'timestamp': datetime.now().isoformat(),
    'config': {
        'model': 'EfficientNetB0',
        'img_size': IMG_SIZE,
        'batch_size': BATCH_SIZE,
        'epochs': EPOCHS,
        'epochs_trained': len(history.history['accuracy']),
        'learning_rate': LEARNING_RATE,
        'training_samples': train_generator.samples,
        'validation_samples': val_generator.samples,
        'num_classes': train_generator.num_classes,
        'classes': list(train_generator.class_indices.keys())
    }
}

with open(HISTORY_PATH, 'w') as f:
    json.dump(history_dict, f, indent=2)
    
print(f"✓ Training history saved to: {HISTORY_PATH}")
print(f"✓ Model saved to: {MODEL_SAVE_PATH}")
