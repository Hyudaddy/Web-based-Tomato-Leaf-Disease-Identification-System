import os
import shutil

def organize_test_data(test_dir):
    """
    Organizes mixed tomato leaf disease images into subfolders based on filenames.
    Mapping logic tailored to the common naming conventions in this dataset.
    """
    # Define mapping from filename keywords to actual folder names used in the model
    # Most models use "Tomato___Class_Name" format
    class_mapping = {
        "BacterialSpot": "Tomato___Bacterial_spot",
        "EarlyBlight": "Tomato___Early_blight",
        "Healthy": "Tomato___healthy",
        "LateBlight": "Tomato___Late_blight",
        "LeafMold": "Tomato___Leaf_Mold",
        "MosaicVirus": "Tomato___Tomato_Mosaic_virus",
        "SeptoriaLeafSpot": "Tomato___Septoria_leaf_spot",
        "SpiderMites": "Tomato___Spider_mites Two-spotted_spider_mite",
        "TargetSpot": "Tomato___Target_Spot",
        "YellowCurlVirus": "Tomato___Tomato_Yellow_Leaf_Curl_Virus"
    }

    print(f"Scanning directory: {test_dir}")
    
    files = [f for f in os.listdir(test_dir) if os.path.isfile(os.path.join(test_dir, f))]
    print(f"Found {len(files)} files to organize.")

    moved_count = 0
    errors = []

    for filename in files:
        # Determine the target folder
        target_folder = None
        for keyword, folder_name in class_mapping.items():
            if keyword.lower() in filename.lower():
                target_folder = folder_name
                break
        
        if not target_folder:
            print(f"⚠️ Could not Determine class for: {filename}")
            continue

        # Create target directory
        target_path = os.path.join(test_dir, target_folder)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            print(f"📁 Created folder: {target_folder}")

        # Move file
        try:
            shutil.move(os.path.join(test_dir, filename), os.path.join(target_path, filename))
            moved_count += 1
        except Exception as e:
            errors.append(f"Error moving {filename}: {str(e)}")

    print(f"\n✅ Organization Complete!")
    print(f"Total moved: {moved_count}")
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for err in errors:
            print(f"  - {err}")

if __name__ == "__main__":
    SOURCE_PATH = r"C:\Users\hewer\Desktop\DATASET\test"
    organize_test_data(SOURCE_PATH)
