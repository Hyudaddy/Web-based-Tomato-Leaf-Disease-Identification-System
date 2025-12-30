#!/usr/bin/env python3
"""
================================================================================
FITO - FIXED EFFICIENTNETB0 TRAINING SCRIPT
================================================================================
This script uses a TWO-STAGE training approach for better accuracy:
1. Train custom layers only (base frozen) - 20 epochs
2. Fine-tune entire model (base unfrozen) - 30 epochs

ESTIMATED TIME: 6-8 hours
"""

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

print("=" * 80)
print("FITO - EFFICIENTNETB0 TWO-STAGE TRAINING (FIXED)")
print("=" * 80)
print("\nLoading libraries...")

print(f"✓ TensorFlow version: {tf.__version__}")

# ================================================================================
# CONFIGURATION
# ================================================================================
print("\n" + "=" * 80)
print("STEP 1: CONFIGURATION")
print("=" * 80)

# Paths
DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")
VAL_PATH = os.path.join(DATASET_PATH, "validation")
MODEL_SAVE_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\trained_model_efficientnet_FIXED.h5"
HISTORY_PATH = r"C:\Users\HYUDADDY\Desktop\TLDI_system\training_history_efficientnet_FIXED.json"

# Hyperparameters
IMG_SIZE = 224
BATCH_SIZE = 16  # Increased for better gradient estimates
STAGE1_EPOCHS = 20  # Train custom layers only
STAGE2_EPOCHS = 30  # Fine-tune entire model
STAGE1_LR = 0.001  # Higher LR for custom layers
STAGE2_LR = 0.0001  # Lower LR for fine-tuning

print(f"""
📋 Training Configuration:
   • Model: EfficientNetB0 (Two-Stage Training)
   • Image Size: {IMG_SIZE}x{IMG_SIZE}
   • Batch Size: {BATCH_SIZE}
   • Stage 1: {STAGE1_EPOCHS} epochs (custom layers only, LR={STAGE1_LR})
   • Stage 2: {STAGE2_EPOCHS} epochs (fine-tune all, LR={STAGE2_LR})
   • Total Epochs: {STAGE1_EPOCHS + STAGE2_EPOCHS}
""")

# Verify paths
if not os.path.exists(TRAIN_PATH):
    print(f"❌ ERROR: Training folder not found at: {TRAIN_PATH}")
    exit(1)
if not os.path.exists(VAL_PATH):
    print(f"❌ ERROR: Validation folder not found at: {VAL_PATH}")
    exit(1)

print("✓ Dataset paths verified")

# ================================================================================
# DATA PREPARATION
# ================================================================================
print("\n" + "=" * 80)
print("STEP 2: DATA PREPARATION")
print("=" * 80)

# Training data with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    brightness_range=[0.8, 1.2],
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest'
)

# Validation data (no augmentation)
val_datagen = ImageDataGenerator(rescale=1./255)

print("Loading training data...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

print("Loading validation data...")
val_generator = val_datagen.flow_from_directory(
    VAL_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

print(f"""
✓ Data loaded:
   • Training samples: {train_generator.samples}
   • Validation samples: {val_generator.samples}
   • Classes: {train_generator.num_classes}
   • Class names: {list(train_generator.class_indices.keys())}
""")

# ================================================================================
# MODEL BUILDING
# ================================================================================
print("\n" + "=" * 80)
print("STEP 3: MODEL BUILDING")
print("=" * 80)

tf.keras.backend.clear_session()

print("Building EfficientNetB0 model...")

# Create input
inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

# Load base model without weights first
base_model = EfficientNetB0(
    weights=None,
    include_top=False,
    input_tensor=inputs
)

print(f"✓ EfficientNetB0 architecture created with {len(base_model.layers)} layers")

# Load ImageNet weights
print("Loading ImageNet weights...")
try:
    weights_path = tf.keras.utils.get_file(
        'efficientnetb0_notop.h5',
        'https://storage.googleapis.com/keras-applications/efficientnetb0_notop.h5',
        cache_subdir='models',
        file_hash=None  # Skip hash to avoid corruption
    )
    base_model.load_weights(weights_path)
    print("✓ ImageNet weights loaded successfully!")
except Exception as e:
    print(f"⚠️ Warning: Could not load ImageNet weights: {e}")
    print("Continuing with random initialization...")

# Freeze base model for Stage 1
base_model.trainable = False

# Add custom classification layers
x = base_model(inputs, training=False)
x = GlobalAveragePooling2D(name='global_avg_pool')(x)
x = BatchNormalization(name='bn1')(x)
x = Dropout(0.5, name='dropout1')(x)  # Increased dropout
x = Dense(512, activation='relu', name='dense1')(x)
x = BatchNormalization(name='bn2')(x)
x = Dropout(0.4, name='dropout2')(x)
x = Dense(256, activation='relu', name='dense2')(x)
x = BatchNormalization(name='bn3')(x)
x = Dropout(0.3, name='dropout3')(x)
outputs = Dense(train_generator.num_classes, activation='softmax', name='output')(x)

# Create model
model = Model(inputs, outputs, name='EfficientNetB0_TomatoDisease')

print("\n📐 Model Architecture:")
model.summary()

trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
total_params = model.count_params()
print(f"""
✓ Model built successfully!
   • Total parameters: {total_params:,}
   • Trainable parameters: {trainable_params:,}
   • Frozen parameters: {total_params - trainable_params:,}
""")

# ================================================================================
# STAGE 1: TRAIN CUSTOM LAYERS ONLY
# ================================================================================
print("\n" + "=" * 80)
print("STAGE 1: TRAINING CUSTOM LAYERS (Base Frozen)")
print("=" * 80)

# Compile for Stage 1
model.compile(
    optimizer=Adam(learning_rate=STAGE1_LR),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Callbacks for Stage 1
stage1_callbacks = [
    ModelCheckpoint(
        MODEL_SAVE_PATH.replace('.h5', '_stage1.h5'),
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    ),
    EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
]

print(f"""
🚀 Starting Stage 1 Training:
   • Epochs: {STAGE1_EPOCHS}
   • Learning Rate: {STAGE1_LR}
   • Base Model: FROZEN
   • Training: Custom layers only
""")

start_time = datetime.now()

history_stage1 = model.fit(
    train_generator,
    epochs=STAGE1_EPOCHS,
    validation_data=val_generator,
    callbacks=stage1_callbacks,
    verbose=1
)

stage1_time = datetime.now() - start_time
print(f"\n✅ Stage 1 completed in {stage1_time}")
print(f"Best validation accuracy: {max(history_stage1.history['val_accuracy'])*100:.2f}%")

# ================================================================================
# STAGE 2: FINE-TUNE ENTIRE MODEL
# ================================================================================
print("\n" + "=" * 80)
print("STAGE 2: FINE-TUNING ENTIRE MODEL (Base Unfrozen)")
print("=" * 80)

# Unfreeze base model
base_model.trainable = True

# Freeze first 100 layers (keep low-level features frozen)
for layer in base_model.layers[:100]:
    layer.trainable = False

trainable_params = sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
print(f"✓ Base model unfrozen (first 100 layers still frozen)")
print(f"   • Trainable parameters: {trainable_params:,}")

# Recompile with lower learning rate
model.compile(
    optimizer=Adam(learning_rate=STAGE2_LR),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Callbacks for Stage 2
stage2_callbacks = [
    ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    ),
    EarlyStopping(
        monitor='val_loss',
        patience=7,
        restore_best_weights=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-8,
        verbose=1
    )
]

print(f"""
🚀 Starting Stage 2 Training:
   • Epochs: {STAGE2_EPOCHS}
   • Learning Rate: {STAGE2_LR}
   • Base Model: PARTIALLY UNFROZEN
   • Training: Entire model (fine-tuning)
""")

stage2_start = datetime.now()

history_stage2 = model.fit(
    train_generator,
    epochs=STAGE2_EPOCHS,
    validation_data=val_generator,
    callbacks=stage2_callbacks,
    verbose=1
)

stage2_time = datetime.now() - stage2_start
total_time = datetime.now() - start_time

print(f"\n✅ Stage 2 completed in {stage2_time}")
print(f"Best validation accuracy: {max(history_stage2.history['val_accuracy'])*100:.2f}%")

# ================================================================================
# FINAL EVALUATION
# ================================================================================
print("\n" + "=" * 80)
print("FINAL EVALUATION")
print("=" * 80)

val_loss, val_accuracy = model.evaluate(val_generator)

print(f"""
📊 FINAL RESULTS:
   ✅ Validation Loss: {val_loss:.4f}
   ✅ Validation Accuracy: {val_accuracy*100:.2f}%
   
   Stage 1 Best: {max(history_stage1.history['val_accuracy'])*100:.2f}%
   Stage 2 Best: {max(history_stage2.history['val_accuracy'])*100:.2f}%
   
   Total Training Time: {total_time}
""")

# ================================================================================
# SAVE TRAINING HISTORY
# ================================================================================
print("\n" + "=" * 80)
print("SAVING TRAINING HISTORY")
print("=" * 80)

# Combine histories
combined_history = {
    'stage1': {
        'accuracy': [float(x) for x in history_stage1.history['accuracy']],
        'loss': [float(x) for x in history_stage1.history['loss']],
        'val_accuracy': [float(x) for x in history_stage1.history['val_accuracy']],
        'val_loss': [float(x) for x in history_stage1.history['val_loss']],
        'best_val_accuracy': float(max(history_stage1.history['val_accuracy'])),
        'duration': str(stage1_time)
    },
    'stage2': {
        'accuracy': [float(x) for x in history_stage2.history['accuracy']],
        'loss': [float(x) for x in history_stage2.history['loss']],
        'val_accuracy': [float(x) for x in history_stage2.history['val_accuracy']],
        'val_loss': [float(x) for x in history_stage2.history['val_loss']],
        'best_val_accuracy': float(max(history_stage2.history['val_accuracy'])),
        'duration': str(stage2_time)
    },
    'final': {
        'val_accuracy': float(val_accuracy),
        'val_loss': float(val_loss),
        'total_duration': str(total_time),
        'timestamp': datetime.now().isoformat()
    },
    'config': {
        'model': 'EfficientNetB0',
        'img_size': IMG_SIZE,
        'batch_size': BATCH_SIZE,
        'stage1_epochs': STAGE1_EPOCHS,
        'stage2_epochs': STAGE2_EPOCHS,
        'stage1_lr': STAGE1_LR,
        'stage2_lr': STAGE2_LR,
        'training_samples': train_generator.samples,
        'validation_samples': val_generator.samples,
        'num_classes': train_generator.num_classes,
        'classes': list(train_generator.class_indices.keys())
    }
}

with open(HISTORY_PATH, 'w') as f:
    json.dump(combined_history, f, indent=2)

print(f"✓ Training history saved to: {HISTORY_PATH}")
print(f"✓ Model saved to: {MODEL_SAVE_PATH}")

# ================================================================================
# COMPLETE
# ================================================================================
print("\n" + "=" * 80)
print("🎉 TRAINING COMPLETE!")
print("=" * 80)

print(f"""
📊 SUMMARY:
   • Final Accuracy: {val_accuracy*100:.2f}%
   • Total Training Time: {total_time}
   • Model saved to: {MODEL_SAVE_PATH}

🔧 NEXT STEPS:
   1. Update model_handler.py line 49:
      image = image.resize((224, 224))
   
   2. Copy the new model:
      copy "{MODEL_SAVE_PATH}" "{os.path.dirname(MODEL_SAVE_PATH)}\\backend\\trained_model_fito.h5"
   
   3. Restart backend server

Expected accuracy: 85-95% (much better than 16.45%!)
""")

print("=" * 80)
print("Training script completed successfully!")
print("=" * 80)
