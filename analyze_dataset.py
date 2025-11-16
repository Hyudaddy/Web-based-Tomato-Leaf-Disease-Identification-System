#!/usr/bin/env python3
"""
Analyze the dataset distribution across classes
Run this BEFORE training to understand your data
"""

import os
from collections import defaultdict

DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
TRAIN_PATH = os.path.join(DATASET_PATH, "training")
VAL_PATH = os.path.join(DATASET_PATH, "validation")

def count_images(path):
    """Count images in each class directory"""
    counts = defaultdict(int)
    
    if not os.path.exists(path):
        print(f"❌ Path does not exist: {path}")
        return counts
    
    for class_name in os.listdir(path):
        class_path = os.path.join(path, class_name)
        if os.path.isdir(class_path):
            image_count = len([f for f in os.listdir(class_path) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])
            counts[class_name] = image_count
    
    return counts

print("=" * 80)
print("DATASET ANALYSIS")
print("=" * 80)

# Analyze training set
print("\n📚 TRAINING SET:")
print("-" * 80)
train_counts = count_images(TRAIN_PATH)
train_total = 0

if train_counts:
    for class_name in sorted(train_counts.keys()):
        count = train_counts[class_name]
        train_total += count
        bar_length = int(count / 10)  # Simple bar chart
        bar = "█" * bar_length
        print(f"  {class_name:50s}: {count:5d} {bar}")
    
    print("-" * 80)
    print(f"  {'TOTAL':50s}: {train_total:5d}")
else:
    print("❌ No training data found!")

# Analyze validation set
print("\n📚 VALIDATION SET:")
print("-" * 80)
val_counts = count_images(VAL_PATH)
val_total = 0

if val_counts:
    for class_name in sorted(val_counts.keys()):
        count = val_counts[class_name]
        val_total += count
        bar_length = int(count / 10)
        bar = "█" * bar_length
        print(f"  {class_name:50s}: {count:5d} {bar}")
    
    print("-" * 80)
    print(f"  {'TOTAL':50s}: {val_total:5d}")
else:
    print("❌ No validation data found!")

# Summary
print("\n" + "=" * 80)
print("📊 SUMMARY:")
print("=" * 80)
print(f"  Total Training Images: {train_total}")
print(f"  Total Validation Images: {val_total}")
print(f"  Total Dataset Size: {train_total + val_total}")
print(f"  Number of Classes: {len(train_counts)}")

# Check balance
if train_counts:
    print("\n" + "=" * 80)
    print("⚖️  CLASS BALANCE ANALYSIS:")
    print("=" * 80)
    
    min_class = min(train_counts.values())
    max_class = max(train_counts.values())
    avg_class = train_total / len(train_counts)
    imbalance_ratio = max_class / min_class if min_class > 0 else 0
    
    print(f"  Min images per class: {min_class}")
    print(f"  Max images per class: {max_class}")
    print(f"  Avg images per class: {avg_class:.1f}")
    print(f"  Imbalance ratio: {imbalance_ratio:.2f}x")
    
    if imbalance_ratio > 3:
        print(f"\n  ⚠️  WARNING: Dataset is HIGHLY imbalanced (>{imbalance_ratio:.1f}x difference)")
        print(f"      Consider using class weights during training")
    elif imbalance_ratio > 2:
        print(f"\n  ⚠️  WARNING: Dataset is imbalanced (>{imbalance_ratio:.1f}x difference)")
        print(f"      Consider using class weights during training")
    else:
        print(f"\n  ✅ Dataset is well-balanced ({imbalance_ratio:.2f}x ratio)")

print("\n" + "=" * 80)
print("✅ Analysis complete! You can now run train_model_optimized.py")
print("=" * 80)
