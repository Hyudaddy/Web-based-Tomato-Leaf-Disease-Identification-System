import requests
import os
import glob

url = "http://localhost:8000/predict"
assets_dir = r"c:\Users\altai\Desktop\TLDI_system\assets"
image_pattern = os.path.join(assets_dir, "*.jpg")

images = glob.glob(image_pattern)
images += glob.glob(os.path.join(assets_dir, "*.png"))

print(f"Found {len(images)} images to test.")

for file_path in images:
    filename = os.path.basename(file_path)
    print(f"\nTesting: {filename}")
    
    try:
        with open(file_path, 'rb') as f:
            # Determine content type based on extension
            content_type = 'image/png' if filename.lower().endswith('.png') else 'image/jpeg'
            
            files = {'file': (filename, f, content_type)}
            response = requests.post(url, files=files)
        
        print(f"Status Code: {response.status_code}")
        try:
            json_response = response.json()
            if response.status_code == 200:
                print(f"SUCCESS: {json_response['prediction']} ({json_response['confidence']:.4f})")
            else:
                print(f"FAILURE: {json_response.get('message', 'Unknown error')} - Confidence: {json_response.get('confidence', 'N/A')}")
        except:
            print(f"Raw Response: {response.text}")

    except Exception as e:
        print(f"Error testing {filename}: {e}")
