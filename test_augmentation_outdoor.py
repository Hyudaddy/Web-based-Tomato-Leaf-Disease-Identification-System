#!/usr/bin/env python3
"""
Test script to visualize the outdoor augmentation effects
This helps you see what the enhanced augmentation does to your images
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from scipy.ndimage import gaussian_filter

# Outdoor noise preprocessing function (same as in training script)
def add_outdoor_noise(image):
    """Simulate outdoor conditions: noise, blur, contrast variations"""
    if np.random.random() < 0.3:
        noise = np.random.normal(0, 0.02, image.shape)
        image = np.clip(image + noise, 0, 1)
    
    if np.random.random() < 0.2:
        sigma = np.random.uniform(0.5, 1.5)
        for i in range(image.shape[2]):
            image[:, :, i] = gaussian_filter(image[:, :, i], sigma=sigma)
    
    if np.random.random() < 0.3:
        alpha = np.random.uniform(0.8, 1.2)
        image = np.clip(alpha * image, 0, 1)
    
    return image

# Configuration
DATASET_PATH = r"C:\Users\altai\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")
IMG_SIZE = 224

# Create augmentation generator (same as training)
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.3,
    zoom_range=0.35,
    brightness_range=[0.5, 1.5],
    channel_shift_range=30.0,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='reflect',
    preprocessing_function=add_outdoor_noise
)

print("=" * 80)
print("OUTDOOR AUGMENTATION TEST - Visualizing Augmentation Effects")
print("=" * 80)

# Get first image from first class
first_class = sorted(os.listdir(TRAIN_PATH))[0]
first_class_path = os.path.join(TRAIN_PATH, first_class)
first_image = [f for f in os.listdir(first_class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))][0]
image_path = os.path.join(first_class_path, first_image)

print(f"\n📸 Using sample image:")
print(f"   • Class: {first_class}")
print(f"   • Image: {first_image}")

# Load and prepare image
img = load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
x = img_to_array(img)
x = x.reshape((1,) + x.shape)

# Generate augmented samples
print(f"\n🔄 Generating 9 augmented versions...")
fig, axes = plt.subplots(3, 3, figsize=(15, 15))
fig.suptitle(f'Outdoor Augmentation Examples - {first_class}', fontsize=16, fontweight='bold')

i = 0
for batch in datagen.flow(x, batch_size=1):
    ax = axes[i // 3, i % 3]
    ax.imshow(batch[0])
    ax.axis('off')
    
    # Add title describing augmentation
    if i == 0:
        ax.set_title('Original + Light Aug', fontsize=10)
    else:
        ax.set_title(f'Augmented #{i}', fontsize=10)
    
    i += 1
    if i >= 9:
        break

plt.tight_layout()
output_path = 'augmentation_test_outdoor.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\n✅ Augmentation visualization saved to: {output_path}")
print(f"\n💡 What to look for in the image:")
print(f"   • Varying brightness (simulates sunlight/shadows)")
print(f"   • Different rotations and angles")
print(f"   • Color shifts (simulates outdoor lighting)")
print(f"   • Slight blur/noise (simulates camera shake)")
print(f"   • Zoomed in/out versions")
print("\n" + "=" * 80)
