import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

# Dataset paths
DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")
VAL_PATH = os.path.join(DATASET_PATH, "validation")
MODEL_SAVE_PATH = r"C:\Users\HYUDADDY\Desktop\TLD_Detection\trained_model_tomato.h5"

# Hyperparameters
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001

print("=" * 60)
print("TOMATO LEAF DISEASE DETECTION - MODEL TRAINING")
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

# Build model using transfer learning
print("\n" + "=" * 60)
print("Building model with MobileNetV2 transfer learning...")
print("=" * 60)

# Load pre-trained MobileNetV2
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# Freeze base model layers
base_model.trainable = False

# Add custom top layers
inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base_model(inputs, training=False)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)
outputs = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs, outputs)

# Compile model
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\nModel Summary:")
model.summary()

# Train model
print("\n" + "=" * 60)
print("Starting training...")
print("=" * 60)

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    verbose=1
)

# Evaluate on validation set
print("\n" + "=" * 60)
print("Evaluating model...")
print("=" * 60)

val_loss, val_accuracy = model.evaluate(val_generator)
print(f"\nValidation Loss: {val_loss:.4f}")
print(f"Validation Accuracy: {val_accuracy:.4f}")

# Save model
print(f"\nSaving model to: {MODEL_SAVE_PATH}")
model.save(MODEL_SAVE_PATH)
print("✓ Model saved successfully!")

print("\n" + "=" * 60)
print("Training complete!")
print("=" * 60)
print(f"\nNew model saved at: {MODEL_SAVE_PATH}")
print("Replace the old trained_model.h5 with this new model to use it in the API.")
