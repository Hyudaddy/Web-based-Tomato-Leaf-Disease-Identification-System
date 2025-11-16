#!/usr/bin/env python3
"""
Download random non-tomato images for the Unidentified class
Uses Bing Image Search to download diverse images
"""

import os
import requests
from pathlib import Path
import time
from urllib.parse import quote

# Configuration
TRAINING_DIR = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\training\Unidentified"
VALIDATION_DIR = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation\Unidentified"

# Search queries for diverse non-tomato images
SEARCH_QUERIES = [
    "human face portrait",
    "random objects",
    "plants not tomato",
    "flowers",
    "grass weeds",
    "food items",
    "buildings architecture",
    "animals wildlife",
    "landscapes nature",
    "paper documents",
    "fabric texture",
    "metal surface",
    "water droplets",
    "tree leaves",
    "fruit apple orange",
]

def download_images_bing(query, output_dir, num_images=30):
    """Download images from Bing Image Search"""
    print(f"\n📥 Downloading images for: {query}")
    
    # Bing Image Search URL
    url = f"https://www.bing.com/images/search?q={quote(query)}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Extract image URLs from the page (basic parsing)
        import re
        image_urls = re.findall(r'"murl":"([^"]+)"', response.text)
        
        if not image_urls:
            print(f"⚠️ No images found for: {query}")
            return 0
        
        downloaded = 0
        for i, img_url in enumerate(image_urls[:num_images]):
            try:
                img_response = requests.get(img_url, timeout=10)
                img_response.raise_for_status()
                
                # Save image
                filename = f"{query.replace(' ', '_')}_{i:03d}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                downloaded += 1
                print(f"  ✓ Downloaded: {filename}")
                
                # Be respectful - add delay
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  ✗ Failed to download image {i}: {str(e)[:50]}")
                continue
        
        print(f"  ✅ Downloaded {downloaded}/{num_images} images")
        return downloaded
        
    except Exception as e:
        print(f"❌ Error searching for '{query}': {str(e)}")
        return 0

def main():
    print("=" * 60)
    print("DOWNLOADING UNIDENTIFIED IMAGES FOR MODEL TRAINING")
    print("=" * 60)
    
    # Create directories if they don't exist
    os.makedirs(TRAINING_DIR, exist_ok=True)
    os.makedirs(VALIDATION_DIR, exist_ok=True)
    
    total_downloaded = 0
    
    # Download images for each query
    for query in SEARCH_QUERIES:
        # 70% to training, 30% to validation
        training_count = download_images_bing(query, TRAINING_DIR, num_images=20)
        validation_count = download_images_bing(query, VALIDATION_DIR, num_images=8)
        
        total_downloaded += training_count + validation_count
    
    print("\n" + "=" * 60)
    print(f"✅ DOWNLOAD COMPLETE!")
    print(f"Total images downloaded: {total_downloaded}")
    print(f"Training folder: {TRAINING_DIR}")
    print(f"Validation folder: {VALIDATION_DIR}")
    print("=" * 60)
    print("\n📝 NEXT STEPS:")
    print("1. Review the downloaded images (optional)")
    print("2. Run: python retrain_model_with_unidentified.py")
    print("3. Wait for retraining to complete (~10-20 minutes)")
    print("4. Test the new model!")

if __name__ == "__main__":
    main()
