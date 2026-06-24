#!/usr/bin/env python3
"""
Organize Kaggle random images into Unidentified training/validation folders
"""

import os
import shutil
import random
from pathlib import Path

# Configuration
SOURCE_DIR = r"C:\Users\HYUDADDY\Downloads\archive\data"
TRAINING_DIR = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\training\Unidentified"
VALIDATION_DIR = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation\Unidentified"

# Supported image formats
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

def find_all_images(root_path):
    """Find all image files in the source directory"""
    print(f"\n🔍 Scanning for images in: {root_path}")
    
    image_files = []
    for file in os.listdir(root_path):
        if Path(file).suffix.lower() in IMAGE_EXTENSIONS:
            full_path = os.path.join(root_path, file)
            image_files.append(full_path)
    
    print(f"✓ Found {len(image_files)} image files")
    return image_files

def organize_images(image_files):
    """Organize images into training/validation folders"""
    
    if len(image_files) == 0:
        print("❌ No images found!")
        return 0
    
    # Create target directories
    os.makedirs(TRAINING_DIR, exist_ok=True)
    os.makedirs(VALIDATION_DIR, exist_ok=True)
    
    # Shuffle for random split
    random.shuffle(image_files)
    
    # Split: 70% training, 30% validation
    split_idx = int(len(image_files) * 0.7)
    training_files = image_files[:split_idx]
    validation_files = image_files[split_idx:]
    
    print(f"\n📊 Splitting images:")
    print(f"  Training: {len(training_files)} images (70%)")
    print(f"  Validation: {len(validation_files)} images (30%)")
    
    # Copy training images
    print(f"\n📋 Copying training images...")
    training_copied = 0
    for i, src_file in enumerate(training_files):
        try:
            ext = Path(src_file).suffix
            filename = f"unidentified_train_{i:05d}{ext}"
            dst_file = os.path.join(TRAINING_DIR, filename)
            shutil.copy2(src_file, dst_file)
            training_copied += 1
            
            if (i + 1) % 100 == 0:
                print(f"  ✓ Copied {i + 1}/{len(training_files)} training images")
        
        except Exception as e:
            print(f"  ✗ Error copying {Path(src_file).name}: {str(e)[:40]}")
    
    print(f"  ✅ Completed: {training_copied} training images")
    
    # Copy validation images
    print(f"\n📋 Copying validation images...")
    validation_copied = 0
    for i, src_file in enumerate(validation_files):
        try:
            ext = Path(src_file).suffix
            filename = f"unidentified_val_{i:05d}{ext}"
            dst_file = os.path.join(VALIDATION_DIR, filename)
            shutil.copy2(src_file, dst_file)
            validation_copied += 1
            
            if (i + 1) % 50 == 0:
                print(f"  ✓ Copied {i + 1}/{len(validation_files)} validation images")
        
        except Exception as e:
            print(f"  ✗ Error copying {Path(src_file).name}: {str(e)[:40]}")
    
    print(f"  ✅ Completed: {validation_copied} validation images")
    
    return training_copied + validation_copied

def main():
    print("=" * 70)
    print("KAGGLE DATASET ORGANIZATION")
    print("=" * 70)
    
    # Check if source directory exists
    if not os.path.exists(SOURCE_DIR):
        print(f"\n❌ ERROR: Source directory not found!")
        print(f"   Expected: {SOURCE_DIR}")
        return
    
    print(f"\n📂 Source: {SOURCE_DIR}")
    print(f"📂 Training destination: {TRAINING_DIR}")
    print(f"📂 Validation destination: {VALIDATION_DIR}")
    
    # Find all images
    image_files = find_all_images(SOURCE_DIR)
    
    if len(image_files) == 0:
        print("\n❌ No images found in the source directory!")
        return
    
    # Organize images
    total_copied = organize_images(image_files)
    
    if total_copied == 0:
        print("\n❌ Failed to copy any images!")
        return
    
    # Verify
    training_count = len([f for f in os.listdir(TRAINING_DIR) if Path(f).suffix.lower() in IMAGE_EXTENSIONS])
    validation_count = len([f for f in os.listdir(VALIDATION_DIR) if Path(f).suffix.lower() in IMAGE_EXTENSIONS])
    
    # Final summary
    print("\n" + "=" * 70)
    print("✅ DATASET ORGANIZATION COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Summary:")
    print(f"  Total images organized: {total_copied}")
    print(f"  Training images: {training_count}")
    print(f"  Validation images: {validation_count}")
    print(f"\n📁 Folders:")
    print(f"  Training: {TRAINING_DIR}")
    print(f"  Validation: {VALIDATION_DIR}")
    
    if training_count >= 150 and validation_count >= 50:
        print(f"\n✅ Perfect! You have enough images for retraining!")
        print(f"\n📝 NEXT STEPS:")
        print(f"1. Run: python retrain_model_with_unidentified.py")
        print(f"2. Wait for retraining (~10-20 minutes)")
        print(f"3. Replace the old model with the new one")
        print(f"4. Test with your face image!")
    else:
        print(f"\n⚠️ WARNING: You may need more images")
        print(f"  Recommended: 200+ training, 80+ validation")
        print(f"  Current: {training_count} training, {validation_count} validation")

if __name__ == "__main__":
    main()
