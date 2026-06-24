"""
================================================================================
FITO - TOMATO LEAF DISEASE DETECTION MODEL TRAINING SCRIPT
================================================================================
Google Colab Version with EfficientNetB0 for Higher Accuracy

INSTRUCTIONS FOR GOOGLE COLAB:
------------------------------
1. Upload your dataset folder to Google Drive:
   - Create folder: My Drive/DATASET/tomato leaf diseases dataset(augmented)/
   - Inside that folder, place your "training" and "validation" folders
   
2. Open Google Colab: https://colab.research.google.com
3. Create new notebook and paste this entire script
4. Enable GPU: Runtime -> Change runtime type -> T4 GPU
5. Run all cells

TRAINING PROCESS FLOW:
----------------------
1. SETUP           - Mount Google Drive and configure GPU
2. CONFIGURATION   - Set hyperparameters (epochs, batch size, learning rate)
3. DATA PREPARATION- Load and augment training/validation images
4. MODEL BUILDING  - Create neural network using transfer learning (EfficientNetB0)
5. TRAINING        - Train the model on the dataset
6. VALIDATION      - Evaluate model performance on unseen data
7. SAVING          - Save trained model and download to local machine

DATASET STRUCTURE REQUIRED:
---------------------------
Google Drive/
└── DATASET/
    └── tomato leaf diseases dataset(augmented)/
        ├── training/
        │   ├── Tomato___Bacterial_spot/
        │   ├── Tomato___Early_blight/
        │   ├── Tomato___Late_blight/
        │   └── ... (other disease folders)
        └── validation/
            ├── Tomato___Bacterial_spot/
            ├── Tomato___Early_blight/
            └── ... (other disease folders)
"""

# ================================================================================
# STEP 1: SETUP - Mount Google Drive and Check GPU
# ================================================================================
# This step connects to your Google Drive where your dataset is stored
# and verifies that GPU acceleration is available for faster training.

print("=" * 80)
print("STEP 1: SETUP - Mounting Google Drive and Checking GPU")
print("=" * 80)

# Mount Google Drive to access your dataset
from google.colab import drive
drive.mount('/content/drive')
print("✓ Google Drive mounted successfully!")

# Check if GPU is available (should show Tesla T4 or similar)
import tensorflow as tf
print(f"\nTensorFlow version: {tf.__version__}")
print(f"GPU Available: {tf.config.list_physical_devices('GPU')}")

# Verify GPU is being used
if tf.config.list_physical_devices('GPU'):
    print("✓ GPU is available and will be used for training!")
    print("  Training will be 10-20x faster than CPU!")
else:
    print("⚠️ WARNING: No GPU detected. Training will be slow.")
    print("  Go to: Runtime -> Change runtime type -> T4 GPU")

# ================================================================================
# IMPORTS - Required libraries for deep learning and data processing
# ================================================================================
print("\n" + "=" * 80)
print("Loading required libraries...")
print("=" * 80)

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0  # Changed from MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

print("✓ All libraries loaded successfully!")

# ================================================================================
# STEP 2: CONFIGURATION - Define paths and hyperparameters
# ================================================================================
# This is where we configure all the settings BEFORE training begins.
# The hyperparameters control HOW the model learns.

print("\n" + "=" * 80)
print("STEP 2: CONFIGURATION - Setting Hyperparameters")
print("=" * 80)

# Dataset paths - GOOGLE DRIVE PATHS
# ==============================================================================
# IMPORTANT: Update these paths if your folder structure is different!
# ==============================================================================
DATASET_PATH = "/content/drive/MyDrive/DATASET/tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")      # Training images (80%)
VAL_PATH = os.path.join(DATASET_PATH, "validation")      # Validation images (20%)

# Output paths - Where to save the trained model
MODEL_SAVE_PATH = "/content/drive/MyDrive/DATASET/trained_model_efficientnet.h5"
HISTORY_PATH = "/content/drive/MyDrive/DATASET/training_history_efficientnet.json"

# HYPERPARAMETERS - These control how the model learns
# ==============================================================================
# These are OPTIMIZED for EfficientNetB0 with GPU training
# ==============================================================================
IMG_SIZE = 224          # Image resolution: 224x224 (optimal for EfficientNet)
BATCH_SIZE = 32         # Number of images processed together (higher with GPU)
EPOCHS = 50             # Number of complete passes through dataset
LEARNING_RATE = 0.001   # How fast the model adjusts weights

# Display configuration
print(f"""
📋 Training Configuration (EfficientNetB0 + GPU):
   • Model: EfficientNetB0 (pre-trained on ImageNet)
   • Image Size: {IMG_SIZE}x{IMG_SIZE} pixels
   • Batch Size: {BATCH_SIZE} images per step
   • Epochs: {EPOCHS} training cycles
   • Learning Rate: {LEARNING_RATE}
   • Device: GPU (Google Colab T4)
   
📁 Dataset Paths:
   • Training: {TRAIN_PATH}
   • Validation: {VAL_PATH}
   
💾 Output Paths:
   • Model: {MODEL_SAVE_PATH}
   • History: {HISTORY_PATH}
""")

# Verify dataset exists
if not os.path.exists(TRAIN_PATH):
    print(f"❌ ERROR: Training folder not found at: {TRAIN_PATH}")
    print("   Please upload your dataset to Google Drive first!")
else:
    print(f"✓ Training folder found!")
    
if not os.path.exists(VAL_PATH):
    print(f"❌ ERROR: Validation folder not found at: {VAL_PATH}")
else:
    print(f"✓ Validation folder found!")

# ================================================================================
# STEP 3: DATA PREPARATION - Configure how images are loaded and augmented
# ================================================================================
# Data augmentation artificially increases dataset variety by creating modified
# versions of images (rotated, flipped, brightness adjusted). This helps the
# model generalize better to real-world images with different lighting/angles.

print("\n" + "=" * 80)
print("STEP 3: DATA PREPARATION - Loading and Augmenting Images")
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
print("Loading training data...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_PATH,                         # Path to training images folder
    target_size=(IMG_SIZE, IMG_SIZE),   # Resize all images to 224x224
    batch_size=BATCH_SIZE,              # Load 32 images at a time
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
""")

# ================================================================================
# STEP 4: MODEL BUILDING - Create the neural network architecture
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
# - Good balance between accuracy and speed

print("\n" + "=" * 80)
print("STEP 4: MODEL BUILDING - Creating EfficientNetB0 Architecture")
print("=" * 80)

# STEP 4A: Load pre-trained EfficientNetB0 (trained on ImageNet - 1.4M+ images)
# This model already knows how to recognize patterns, edges, textures, etc.
print("Loading EfficientNetB0 pre-trained weights from ImageNet...")
base_model = EfficientNetB0(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),  # 224x224 RGB images
    include_top=False,                     # Remove original classification layer
    weights='imagenet'                     # Use pre-trained ImageNet weights
)
print(f"✓ EfficientNetB0 loaded with {len(base_model.layers)} layers")

# STEP 4B: Freeze base model - Don't retrain the pre-trained layers
# We only want to train our custom layers on top
base_model.trainable = False
print("✓ Base model layers frozen (only custom layers will be trained)")

# STEP 4C: Add custom classification layers for tomato disease detection
# This is where we customize for our specific 11-class problem
print("Building custom classification head...")
inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base_model(inputs, training=False)    # Pass through EfficientNetB0

# Global Average Pooling - Reduces feature maps to 1D vector
x = GlobalAveragePooling2D()(x)

# Batch Normalization - Stabilizes and speeds up training
x = BatchNormalization()(x)

# Dropout - Randomly disable 40% of neurons (prevents overfitting)
x = Dropout(0.4)(x)

# Fully connected layer: 512 neurons with ReLU activation
x = Dense(512, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.3)(x)

# Fully connected layer: 256 neurons
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)

# Output layer: 11 classes with softmax activation
# Softmax converts outputs to probabilities that sum to 1
outputs = Dense(train_generator.num_classes, activation='softmax')(x)

# Create the final model
model = Model(inputs, outputs)

# STEP 4D: Compile model - Define how it learns
print("Compiling model...")
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),  # Adam optimizer
    loss='categorical_crossentropy',               # Loss for multi-class
    metrics=['accuracy']                           # Track accuracy
)

print("\n📐 Model Architecture Summary:")
model.summary()

print(f"""
✓ Model built successfully!
   • Base model: EfficientNetB0 (frozen)
   • Custom layers: GlobalPooling -> Dense(512) -> Dense(256) -> Output({train_generator.num_classes})
   • Total parameters: {model.count_params():,}
   • Trainable parameters: {sum([tf.keras.backend.count_params(w) for w in model.trainable_weights]):,}
""")

# ================================================================================
# STEP 5: TRAINING - Train the model on the dataset
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
print("STEP 5: TRAINING - Starting Model Training")
print("=" * 80)

# CALLBACKS - Special functions that run during training
# These help optimize training and save the best model
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
    # This helps the model fine-tune in later epochs
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,                # Reduce LR by half
        patience=3,                # Wait 3 epochs before reducing
        min_lr=1e-7,
        verbose=1
    )
]

print(f"""
🚀 Starting Training:
   • Epochs: {EPOCHS}
   • Batch size: {BATCH_SIZE}
   • Steps per epoch: {train_generator.samples // BATCH_SIZE}
   • Early stopping patience: 7 epochs
   
⏱️ Estimated time: 15-30 minutes with GPU
""")

# *** THIS IS WHERE THE ACTUAL TRAINING HAPPENS ***
# model.fit() - THE MAIN TRAINING FUNCTION
# Each epoch: model processes all training images in batches
# After each epoch: evaluate on validation images to track progress
history = model.fit(
    train_generator,              # Training data
    epochs=EPOCHS,                # Train for 50 epochs (or until early stop)
    validation_data=val_generator,  # Validation data to monitor overfitting
    callbacks=callbacks,          # Run checkpoint, early stop, LR reduction
    verbose=1                     # Show progress bar
)

print("\n✅ Training completed!")

# ================================================================================
# STEP 6: VALIDATION/EVALUATION - Evaluate the trained model
# ================================================================================
# After training, we evaluate the model on the validation set one final time
# to get the official accuracy metrics.

print("\n" + "=" * 80)
print("STEP 6: VALIDATION - Evaluating Model Performance")
print("=" * 80)

# Evaluate the model on validation data
val_loss, val_accuracy = model.evaluate(val_generator)

print(f"""
📊 FINAL RESULTS:
   ✅ Validation Loss: {val_loss:.4f}
   ✅ Validation Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)
   
   Epochs trained: {len(history.history['accuracy'])}
   Best validation accuracy: {max(history.history['val_accuracy'])*100:.2f}%
""")

# ================================================================================
# STEP 7: VISUALIZATION - Plot training history
# ================================================================================
# These plots help you understand how training progressed and whether
# the model overfit or underfit.

print("\n" + "=" * 80)
print("STEP 7: VISUALIZATION - Plotting Training History")
print("=" * 80)

# Create plots
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot accuracy
axes[0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
axes[0].set_title('Model Accuracy Over Epochs', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot loss
axes[1].plot(history.history['loss'], label='Training Loss', linewidth=2)
axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[1].set_title('Model Loss Over Epochs', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/content/drive/MyDrive/DATASET/training_plots.png', dpi=300)
plt.show()

print("✓ Training plots saved to Google Drive!")

# ================================================================================
# STEP 8: SAVE TRAINING HISTORY - Save metrics for documentation
# ================================================================================

print("\n" + "=" * 80)
print("STEP 8: SAVING - Saving Training History")
print("=" * 80)

# Save training history as JSON
history_dict = {
    'accuracy': [float(x) for x in history.history['accuracy']],
    'loss': [float(x) for x in history.history['loss']],
    'val_accuracy': [float(x) for x in history.history['val_accuracy']],
    'val_loss': [float(x) for x in history.history['val_loss']],
    'final_val_accuracy': float(val_accuracy),
    'final_val_loss': float(val_loss),
    'timestamp': datetime.now().isoformat(),
    'config': {
        'model': 'EfficientNetB0',
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
    
print(f"✓ Training history saved to: {HISTORY_PATH}")
print(f"✓ Model saved to: {MODEL_SAVE_PATH}")

# ================================================================================
# COMPLETE! - Summary and Next Steps
# ================================================================================

print("\n" + "=" * 80)
print("🎉 TRAINING COMPLETE!")
print("=" * 80)

print(f"""
📊 TRAINING SUMMARY:
   • Model: EfficientNetB0 (Transfer Learning)
   • Final Accuracy: {val_accuracy*100:.2f}%
   • Epochs Trained: {len(history.history['accuracy'])}
   • Training Time: Check Colab execution log

📁 SAVED FILES (in Google Drive):
   1. trained_model_efficientnet.h5 - The trained model
   2. training_history_efficientnet.json - Training metrics
   3. training_plots.png - Accuracy/loss graphs

📥 NEXT STEPS:
   1. Download the .h5 model file from Google Drive
   2. Copy it to your backend folder:
      C:\\Users\\HYUDADDY\\Desktop\\TLDI_system\\backend\\
   3. Rename it to: trained_model_fito.h5
   4. Restart your backend server

🔧 TO USE THE NEW MODEL:
   - Replace the old trained_model_fito.h5 with the new one
   - The backend will automatically use the new model

📌 FOR YOUR PANEL DEFENSE:
   - EfficientNetB0 is more accurate than MobileNetV2
   - Transfer learning leverages ImageNet pre-training
   - 50 epochs provides thorough training
   - GPU training is ~10-20x faster than CPU
""")

# Download the model to local machine (optional)
print("\n📥 To download the model to your computer:")
print("   - Go to Google Drive in your browser")
print("   - Navigate to: DATASET/trained_model_efficientnet.h5")
print("   - Right-click -> Download")
