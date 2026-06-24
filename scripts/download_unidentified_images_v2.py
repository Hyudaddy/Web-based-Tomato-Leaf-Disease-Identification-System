#!/usr/bin/env python3
"""
Alternative method: Download images from ImageNet or create synthetic unidentified images
This version uses urllib and handles downloads more reliably
"""

import os
import urllib.request
import urllib.error
from pathlib import Path
import time
from PIL import Image, ImageDraw, ImageFilter
import random

# Configuration
TRAINING_DIR = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\training\Unidentified"
VALIDATION_DIR = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation\Unidentified"

# Image URLs from public sources (these are more reliable)
IMAGE_URLS = [
    # Faces
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1024px-Cat_November_2010-1a.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/VAN_CAT.png/1024px-VAN_CAT.png",
    # Objects
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/GoldenGateBridge-001.jpg/1280px-GoldenGateBridge-001.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1024px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
    # More diverse images
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/1024px-Camponotus_flavomarginatus_ant.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Altja_joa_waterfall.jpg/1024px-Altja_joa_waterfall.jpg",
]

def download_image(url, output_path, timeout=10):
    """Download a single image from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        print(f"  ✗ Failed to download: {str(e)[:50]}")
        return False

def generate_synthetic_image(output_path):
    """Generate a synthetic non-tomato image"""
    try:
        # Create random colored image
        width, height = 128, 128
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        img = Image.new('RGB', (width, height), color)
        
        # Add some random shapes and patterns
        draw = ImageDraw.Draw(img)
        for _ in range(random.randint(3, 8)):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.rectangle([x1, y1, x2, y2], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        # Add some blur
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        img.save(output_path, 'JPEG')
        return True
    except Exception as e:
        print(f"  ✗ Failed to generate: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("DOWNLOADING UNIDENTIFIED IMAGES (Alternative Method)")
    print("=" * 60)
    
    # Create directories
    os.makedirs(TRAINING_DIR, exist_ok=True)
    os.makedirs(VALIDATION_DIR, exist_ok=True)
    
    total_downloaded = 0
    
    print("\n📥 Downloading images from public sources...")
    for i, url in enumerate(IMAGE_URLS):
        try:
            filename = f"image_{i:03d}.jpg"
            
            # 70% training, 30% validation
            if random.random() < 0.7:
                output_path = os.path.join(TRAINING_DIR, filename)
                folder = "training"
            else:
                output_path = os.path.join(VALIDATION_DIR, filename)
                folder = "validation"
            
            if download_image(url, output_path):
                print(f"  ✓ Downloaded to {folder}: {filename}")
                total_downloaded += 1
            
            time.sleep(0.5)
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:50]}")
    
    print(f"\n✓ Downloaded {total_downloaded} real images")
    
    # Generate synthetic images to reach target count
    print("\n🎨 Generating synthetic images to reach target count...")
    
    target_training = 280
    target_validation = 120
    
    current_training = len(os.listdir(TRAINING_DIR))
    current_validation = len(os.listdir(VALIDATION_DIR))
    
    print(f"Current: {current_training} training, {current_validation} validation")
    print(f"Target: {target_training} training, {target_validation} validation")
    
    # Generate training images
    for i in range(current_training, target_training):
        filename = f"synthetic_{i:03d}.jpg"
        output_path = os.path.join(TRAINING_DIR, filename)
        if generate_synthetic_image(output_path):
            if (i - current_training) % 50 == 0:
                print(f"  ✓ Generated {i - current_training}/{target_training - current_training} training images")
    
    # Generate validation images
    for i in range(current_validation, target_validation):
        filename = f"synthetic_{i:03d}.jpg"
        output_path = os.path.join(VALIDATION_DIR, filename)
        if generate_synthetic_image(output_path):
            if (i - current_validation) % 30 == 0:
                print(f"  ✓ Generated {i - current_validation}/{target_validation - current_validation} validation images")
    
    final_training = len(os.listdir(TRAINING_DIR))
    final_validation = len(os.listdir(VALIDATION_DIR))
    
    print("\n" + "=" * 60)
    print("✅ IMAGE COLLECTION COMPLETE!")
    print("=" * 60)
    print(f"\nFinal counts:")
    print(f"  Training images: {final_training}")
    print(f"  Validation images: {final_validation}")
    print(f"  Total: {final_training + final_validation}")
    print(f"\nTraining folder: {TRAINING_DIR}")
    print(f"Validation folder: {VALIDATION_DIR}")
    
    print("\n📝 NEXT STEPS:")
    print("1. (Optional) Add more real images manually:")
    print(f"   - Copy images to: {TRAINING_DIR}")
    print(f"   - Or: {VALIDATION_DIR}")
    print("2. Run: python retrain_model_with_unidentified.py")
    print("3. Wait for retraining (~10-20 minutes)")
    print("4. Test the new model!")

if __name__ == "__main__":
    main()
