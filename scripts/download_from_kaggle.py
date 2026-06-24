#!/usr/bin/env python3
"""
Download images from Kaggle dataset and organize for Unidentified class
Requires: pip install kaggle

Setup:
1. Install kaggle: pip install kaggle
2. Download API key from https://www.kaggle.com/settings/account
3. Place kaggle.json in C:\Users\HYUDADDY\.kaggle\
4. Run this script
"""

import os
import shutil
import random
from pathlib import Path

# Configuration
DATASET_NAME = "pankajkumar2002/random-image-sample-dataset"
DOWNLOAD_DIR = r"C:\Users\HYUDADDY\Desktop\kaggle_download"
TRAINING_DIR = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\training\Unidentified"
VALIDATION_DIR = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation\Unidentified"

def setup_kaggle():
    """Check if Kaggle is installed and configured"""
    try:
        import kaggle
        print("✓ Kaggle library found")
        return True
    except ImportError:
        print("❌ Kaggle not installed")
        print("Install with: pip install kaggle")
        return False

def download_kaggle_dataset():
    """Download dataset from Kaggle"""
    print(f"\n📥 Downloading dataset: {DATASET_NAME}")
    print("This may take a few minutes...")
    
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        # Authenticate
        api = KaggleApi()
        api.authenticate()
        
        # Create download directory
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        
        # Download dataset
        api.dataset_download_files(DATASET_NAME, path=DOWNLOAD_DIR, unzip=True)
        print("✓ Dataset downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading: {str(e)}")
        return False

def organize_images():
    """Organize downloaded images into training/validation folders"""
    print("\n📁 Organizing images...")
    
    # Create target directories
    os.makedirs(TRAINING_DIR, exist_ok=True)
    os.makedirs(VALIDATION_DIR, exist_ok=True)
    
    # Find all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_files = []
    
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                image_files.append(os.path.join(root, file))
    
    print(f"Found {len(image_files)} images")
    
    if len(image_files) == 0:
        print("⚠️ No images found in downloaded dataset")
        return 0
    
    # Shuffle and split
    random.shuffle(image_files)
    split_idx = int(len(image_files) * 0.7)
    
    training_files = image_files[:split_idx]
    validation_files = image_files[split_idx:]
    
    print(f"\nSplitting into:")
    print(f"  Training: {len(training_files)} images (70%)")
    print(f"  Validation: {len(validation_files)} images (30%)")
    
    # Copy training images
    print("\n📋 Copying training images...")
    for i, src_file in enumerate(training_files):
        try:
            filename = f"kaggle_train_{i:04d}{Path(src_file).suffix}"
            dst_file = os.path.join(TRAINING_DIR, filename)
            shutil.copy2(src_file, dst_file)
            
            if (i + 1) % 50 == 0:
                print(f"  ✓ Copied {i + 1}/{len(training_files)}")
        except Exception as e:
            print(f"  ✗ Error copying {src_file}: {str(e)[:50]}")
    
    print(f"  ✓ Completed: {len(training_files)} training images")
    
    # Copy validation images
    print("\n📋 Copying validation images...")
    for i, src_file in enumerate(validation_files):
        try:
            filename = f"kaggle_val_{i:04d}{Path(src_file).suffix}"
            dst_file = os.path.join(VALIDATION_DIR, filename)
            shutil.copy2(src_file, dst_file)
            
            if (i + 1) % 30 == 0:
                print(f"  ✓ Copied {i + 1}/{len(validation_files)}")
        except Exception as e:
            print(f"  ✗ Error copying {src_file}: {str(e)[:50]}")
    
    print(f"  ✓ Completed: {len(validation_files)} validation images")
    
    return len(training_files) + len(validation_files)

def cleanup():
    """Clean up downloaded files"""
    print("\n🧹 Cleaning up temporary files...")
    try:
        shutil.rmtree(DOWNLOAD_DIR)
        print("✓ Temporary files removed")
    except Exception as e:
        print(f"⚠️ Could not remove temp files: {str(e)}")

def main():
    print("=" * 60)
    print("KAGGLE DATASET DOWNLOAD & ORGANIZATION")
    print("=" * 60)
    
    # Check Kaggle setup
    if not setup_kaggle():
        print("\n❌ Setup required:")
        print("1. Install: pip install kaggle")
        print("2. Download API key from: https://www.kaggle.com/settings/account")
        print("3. Place kaggle.json in: C:\\Users\\HYUDADDY\\.kaggle\\")
        print("4. Run this script again")
        return
    
    # Download dataset
    if not download_kaggle_dataset():
        print("\n❌ Download failed. Check your Kaggle setup.")
        return
    
    # Organize images
    total = organize_images()
    
    if total == 0:
        print("\n❌ No images were organized")
        return
    
    # Cleanup
    cleanup()
    
    # Final summary
    print("\n" + "=" * 60)
    print("✅ KAGGLE DATASET READY!")
    print("=" * 60)
    print(f"\nTotal images organized: {total}")
    print(f"Training folder: {TRAINING_DIR}")
    print(f"Validation folder: {VALIDATION_DIR}")
    
    # Verify counts
    training_count = len(os.listdir(TRAINING_DIR))
    validation_count = len(os.listdir(VALIDATION_DIR))
    
    print(f"\nFinal counts:")
    print(f"  Training: {training_count} images")
    print(f"  Validation: {validation_count} images")
    
    print("\n📝 NEXT STEPS:")
    print("1. Verify image counts above")
    print("2. Run: python retrain_model_with_unidentified.py")
    print("3. Wait for retraining (~10-20 minutes)")
    print("4. Test the new model!")

if __name__ == "__main__":
    main()
