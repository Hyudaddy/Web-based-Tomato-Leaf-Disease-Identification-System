"""
Script to compare class order between training data and model handler
"""
import os

# Training data path
DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")

# Class names from model_handler.py
model_handler_classes = [
    'Bacterial Spot',
    'Early Blight',
    'Late Blight',
    'Leaf Mold',
    'Septoria Leaf Spot',
    'Spider Mites',
    'Target Spot',
    'Yellow Leaf Curl Virus',
    'Mosaic Virus',
    'Healthy',
    'Unidentified'
]

# Get folder names from training data (alphabetically sorted - as Keras does)
training_folders = sorted([d for d in os.listdir(TRAIN_PATH) if os.path.isdir(os.path.join(TRAIN_PATH, d))])

print("=" * 80)
print("CLASS ORDER COMPARISON")
print("=" * 80)

print("\n1. Training folder classes (Keras alphabetical order):")
for i, folder in enumerate(training_folders):
    print(f"   {i}: {folder}")

print("\n2. Model handler class names (current order):")
for i, class_name in enumerate(model_handler_classes):
    print(f"   {i}: {class_name}")

print("\n" + "=" * 80)
print("ANALYSIS")
print("=" * 80)

# Map folder names to expected class names
folder_to_expected_class = {
    'Tomato___Bacterial_spot': 'Bacterial Spot',
    'Tomato___Early_blight': 'Early Blight',
    'Tomato___Late_blight': 'Late Blight',
    'Tomato___Leaf_Mold': 'Leaf Mold',
    'Tomato___Septoria_leaf_spot': 'Septoria Leaf Spot',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Spider Mites',
    'Tomato___Target_Spot': 'Target Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Yellow Leaf Curl Virus',
    'Tomato___Tomato_mosaic_virus': 'Mosaic Virus',
    'Tomato___healthy': 'Healthy',
    'Unidentified': 'Unidentified'
}

print("\nExpected class order based on training folders:")
expected_class_order = []
for i, folder in enumerate(training_folders):
    expected_class = folder_to_expected_class.get(folder, f"UNKNOWN: {folder}")
    expected_class_order.append(expected_class)
    print(f"   {i}: {expected_class}")

print("\n" + "=" * 80)
print("MISMATCH CHECK")
print("=" * 80)

mismatches = []
for i, (expected, actual) in enumerate(zip(expected_class_order, model_handler_classes)):
    if expected != actual:
        mismatches.append((i, expected, actual))
        print(f"   MISMATCH at index {i}:")
        print(f"      Expected (from training): {expected}")
        print(f"      Actual (model_handler):    {actual}")

if mismatches:
    print(f"\n[WARNING] CRITICAL: Found {len(mismatches)} class order mismatches!")
    print("   This means predictions are being mapped to WRONG class names!")
else:
    print("\n[OK] No mismatches found - class order is correct.")
