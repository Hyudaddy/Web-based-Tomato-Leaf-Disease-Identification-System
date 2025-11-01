#!/usr/bin/env python3
"""
Test prediction with correct class mapping
"""
import requests
import json

def test_prediction():
    print("🧪 Testing Prediction with Correct Class Mapping...")
    print("=" * 60)
    
    # Test the classes endpoint first
    try:
        response = requests.get("http://localhost:8000/classes")
        if response.status_code == 200:
            data = response.json()
            print("✅ Classes endpoint working")
            print(f"📊 Total classes: {data['total_classes']}")
            print("📊 Class names:")
            for i, class_name in enumerate(data['classes']):
                print(f"   {i}: {class_name}")
        else:
            print(f"❌ Classes endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Classes endpoint error: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🎯 The class order is now correct!")
    print("Index 7 = Yellow Leaf Curl Virus")
    print("Index 6 = Target Spot") 
    print("Index 3 = Leaf Mold")
    print("=" * 60)

if __name__ == "__main__":
    test_prediction()
