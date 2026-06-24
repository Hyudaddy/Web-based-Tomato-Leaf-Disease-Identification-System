"""
Test script to verify model predictions and check for bias
Tests images from each disease class against the running FastAPI server
"""
import requests
import os
import random
import json
from collections import defaultdict

# Configuration
API_URL = "http://localhost:8000/predict"
DATASET_PATH = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation"

# Number of images to test per class
IMAGES_PER_CLASS = 5

def get_sample_images(dataset_path, images_per_class=5):
    """Get random sample images from each class folder"""
    samples = {}
    
    for class_folder in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_folder)
        if os.path.isdir(class_path):
            # Get all image files
            images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            # Random sample
            if len(images) > images_per_class:
                selected = random.sample(images, images_per_class)
            else:
                selected = images[:images_per_class]
            
            samples[class_folder] = [os.path.join(class_path, img) for img in selected]
    
    return samples

def test_prediction(image_path):
    """Send image to API and get prediction"""
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(API_URL, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('prediction'), data.get('confidence')
        elif response.status_code == 400:
            # Unidentified
            return 'Unidentified', 0.0
        else:
            return None, None
    except Exception as e:
        print(f"   Error: {e}")
        return None, None

def main():
    print("=" * 80)
    print("MODEL PREDICTION BIAS TEST")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"Dataset: {DATASET_PATH}")
    print(f"Images per class: {IMAGES_PER_CLASS}")
    print()
    
    # Check API is running
    try:
        r = requests.get("http://localhost:8000/health", timeout=5)
        if r.status_code != 200:
            print("[ERROR] API not responding. Make sure backend is running.")
            return
        print("[OK] API is running")
    except:
        print("[ERROR] Cannot connect to API at localhost:8000")
        return
    
    # Get sample images
    print("\nLoading sample images...")
    samples = get_sample_images(DATASET_PATH, IMAGES_PER_CLASS)
    print(f"Found {len(samples)} classes\n")
    
    # Test each class
    results = defaultdict(list)
    prediction_counts = defaultdict(int)
    
    print("-" * 80)
    print("TESTING PREDICTIONS")
    print("-" * 80)
    
    for true_class, image_paths in samples.items():
        # Clean up class name for display
        display_class = true_class.replace("Tomato___", "").replace("_", " ")
        print(f"\nTrue Class: {display_class}")
        
        for img_path in image_paths:
            prediction, confidence = test_prediction(img_path)
            if prediction:
                results[true_class].append({
                    'predicted': prediction,
                    'confidence': confidence,
                    'correct': display_class.lower() in prediction.lower() or prediction.lower() in display_class.lower()
                })
                prediction_counts[prediction] += 1
                
                status = "[OK]" if results[true_class][-1]['correct'] else "[WRONG]"
                print(f"   {status} Predicted: {prediction} ({confidence*100:.1f}%)")
    
    # Summary
    print("\n" + "=" * 80)
    print("PREDICTION DISTRIBUTION SUMMARY")
    print("=" * 80)
    
    total = sum(prediction_counts.values())
    print(f"\nTotal predictions: {total}")
    print("\nPrediction counts (sorted by frequency):")
    
    for pred, count in sorted(prediction_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total) * 100 if total > 0 else 0
        bar = "#" * int(pct / 2)
        print(f"   {pred:30s} {count:3d} ({pct:5.1f}%) {bar}")
    
    # Check for Early Blight bias
    early_blight_count = prediction_counts.get('Early Blight', 0)
    expected_count = total / len(samples) if samples else 0
    
    print("\n" + "=" * 80)
    print("EARLY BLIGHT BIAS CHECK")
    print("=" * 80)
    
    print(f"\nEarly Blight predictions: {early_blight_count}")
    print(f"Expected if balanced: {expected_count:.1f}")
    
    if early_blight_count > expected_count * 1.5:
        print("\n[WARNING] POSSIBLE BIAS: Early Blight is over-predicted!")
        print(f"   Predicted {early_blight_count} times vs expected {expected_count:.1f}")
    elif early_blight_count < expected_count * 0.5:
        print("\n[INFO] Early Blight is under-predicted (model may miss it)")
    else:
        print("\n[OK] Early Blight predictions appear balanced")
    
    # Per-class accuracy
    print("\n" + "=" * 80)
    print("PER-CLASS ACCURACY")
    print("=" * 80)
    
    for true_class in sorted(results.keys()):
        preds = results[true_class]
        correct = sum(1 for p in preds if p['correct'])
        total_class = len(preds)
        accuracy = (correct / total_class * 100) if total_class > 0 else 0
        display_class = true_class.replace("Tomato___", "").replace("_", " ")
        
        status = "[OK]" if accuracy >= 80 else "[LOW]"
        print(f"   {status} {display_class:35s} {correct}/{total_class} = {accuracy:.0f}%")

if __name__ == "__main__":
    main()
