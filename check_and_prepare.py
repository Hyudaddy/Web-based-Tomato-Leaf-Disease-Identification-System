#!/usr/bin/env python3
"""
Pre-training checklist: Verify everything is ready before training
"""

import os
import sys

print("=" * 80)
print("PRE-TRAINING CHECKLIST")
print("=" * 80)

checks_passed = 0
checks_total = 0

# Check 1: Dataset paths exist
print("\n1️⃣  Checking dataset paths...")
checks_total += 1

DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")
VAL_PATH = os.path.join(DATASET_PATH, "validation")

if os.path.exists(TRAIN_PATH):
    print(f"   ✅ Training path exists: {TRAIN_PATH}")
    checks_passed += 1
else:
    print(f"   ❌ Training path NOT found: {TRAIN_PATH}")

if os.path.exists(VAL_PATH):
    print(f"   ✅ Validation path exists: {VAL_PATH}")
else:
    print(f"   ❌ Validation path NOT found: {VAL_PATH}")

# Check 2: Classes exist
print("\n2️⃣  Checking classes...")
checks_total += 1

expected_classes = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy',
    'Unidentified'
]

train_classes = set(os.listdir(TRAIN_PATH)) if os.path.exists(TRAIN_PATH) else set()
missing_classes = set(expected_classes) - train_classes

if not missing_classes:
    print(f"   ✅ All {len(expected_classes)} classes found in training set")
    checks_passed += 1
else:
    print(f"   ⚠️  Missing classes: {missing_classes}")

# Check 3: Count images
print("\n3️⃣  Counting images...")
checks_total += 1

def count_images(path):
    total = 0
    for class_name in os.listdir(path):
        class_path = os.path.join(path, class_name)
        if os.path.isdir(class_path):
            count = len([f for f in os.listdir(class_path) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
            total += count
    return total

train_count = count_images(TRAIN_PATH) if os.path.exists(TRAIN_PATH) else 0
val_count = count_images(VAL_PATH) if os.path.exists(VAL_PATH) else 0
total_count = train_count + val_count

print(f"   Training images: {train_count}")
print(f"   Validation images: {val_count}")
print(f"   Total images: {total_count}")

if total_count > 1000:
    print(f"   ✅ Good dataset size ({total_count} images)")
    checks_passed += 1
elif total_count > 500:
    print(f"   ⚠️  Small dataset ({total_count} images) - may affect accuracy")
else:
    print(f"   ❌ Very small dataset ({total_count} images) - not enough for training")

# Check 4: Backend model path
print("\n4️⃣  Checking backend paths...")
checks_total += 1

backend_path = r"C:\Users\HYUDADDY\Desktop\TLDI_system\backend"
model_path = os.path.join(backend_path, "trained_model_fito.h5")

if os.path.exists(backend_path):
    print(f"   ✅ Backend directory exists")
    checks_passed += 1
else:
    print(f"   ❌ Backend directory NOT found: {backend_path}")

if os.path.exists(model_path):
    model_size = os.path.getsize(model_path) / (1024*1024)  # MB
    print(f"   ✅ Current model found ({model_size:.1f} MB)")
else:
    print(f"   ⚠️  Current model not found at: {model_path}")

# Check 5: Disk space
print("\n5️⃣  Checking disk space...")
checks_total += 1

import shutil
disk_usage = shutil.disk_usage("C:\\")
free_space_gb = disk_usage.free / (1024**3)

if free_space_gb > 2:
    print(f"   ✅ Sufficient disk space ({free_space_gb:.1f} GB free)")
    checks_passed += 1
else:
    print(f"   ⚠️  Low disk space ({free_space_gb:.1f} GB free) - may cause issues")

# Check 6: Python packages
print("\n6️⃣  Checking required packages...")
checks_total += 1

required_packages = ['tensorflow', 'keras', 'numpy', 'PIL']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
        print(f"   ✅ {package} installed")
    except ImportError:
        print(f"   ❌ {package} NOT installed")
        missing_packages.append(package)

if not missing_packages:
    checks_passed += 1
else:
    print(f"\n   Install missing packages with:")
    print(f"   pip install {' '.join(missing_packages)}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nChecks passed: {checks_passed}/{checks_total}")

if checks_passed == checks_total:
    print("\n✅ ALL CHECKS PASSED! Ready to train!")
    print("\nRun: python train_model_optimized.py")
    sys.exit(0)
elif checks_passed >= checks_total - 1:
    print("\n⚠️  MOSTLY READY - Minor issues detected")
    print("You can proceed but may encounter issues")
    sys.exit(0)
else:
    print("\n❌ ISSUES DETECTED - Fix before training")
    sys.exit(1)
