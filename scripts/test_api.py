#!/usr/bin/env python3
"""
Test script for Fito API
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Fito API...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test classes endpoint
    try:
        response = requests.get(f"{base_url}/classes")
        if response.status_code == 200:
            data = response.json()
            print("✅ Classes endpoint working")
            print(f"   Total classes: {data['total_classes']}")
            print(f"   Classes: {data['classes']}")
        else:
            print(f"❌ Classes endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Classes endpoint error: {e}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 API is ready for testing!")
    print("Frontend: http://localhost:3000")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 50)

if __name__ == "__main__":
    test_api()
