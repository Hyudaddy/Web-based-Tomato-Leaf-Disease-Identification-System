"""
Prepare Test Dataset
--------------------
Copies 50 images per class from the Validation set into the Test folder.
Existing images in the test folder are cleared first so we get a clean slate.
"""

import os
import shutil
import random

# ── Configuration ──────────────────────────────────────────────────────────────
SOURCE_VAL  = r"C:\Users\hewer\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation"
DEST_TEST   = r"C:\Users\hewer\Desktop\DATASET\test"
IMAGES_PER_CLASS = 50
SEED = 42          # Fixed seed so results are reproducible
# ───────────────────────────────────────────────────────────────────────────────

# Map validation folder names → test folder names
# (Handles the capitalisation difference for Mosaic Virus)
NAME_MAP = {
    "Tomato___Bacterial_spot":                          "Tomato___Bacterial_spot",
    "Tomato___Early_blight":                            "Tomato___Early_blight",
    "Tomato___Late_blight":                             "Tomato___Late_blight",
    "Tomato___Leaf_Mold":                               "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot":                      "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite":    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot":                             "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus":           "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus":                     "Tomato___Tomato_Mosaic_virus",   # note capital M in test
    "Tomato___healthy":                                 "Tomato___healthy",
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

random.seed(SEED)

print("=" * 60)
print("  PREPARING TEST DATASET")
print("=" * 60)

total_copied = 0

for val_class, test_class in NAME_MAP.items():
    src_dir  = os.path.join(SOURCE_VAL, val_class)
    dest_dir = os.path.join(DEST_TEST, test_class)

    if not os.path.isdir(src_dir):
        print(f"[WARNING] Source not found: {src_dir}")
        continue

    # ── Clear existing test images for this class ────────────────────────────
    if os.path.exists(dest_dir):
        for f in os.listdir(dest_dir):
            if os.path.splitext(f)[1].lower() in IMAGE_EXTS:
                os.remove(os.path.join(dest_dir, f))
    else:
        os.makedirs(dest_dir)

    # ── Sample images from validation ────────────────────────────────────────
    all_images = [
        f for f in os.listdir(src_dir)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTS
    ]

    sample = random.sample(all_images, min(IMAGES_PER_CLASS, len(all_images)))

    for img in sample:
        shutil.copy2(os.path.join(src_dir, img), os.path.join(dest_dir, img))

    total_copied += len(sample)
    print(f"  OK  {test_class:55s}  ->  {len(sample)} images")

print("-" * 60)
print(f"  Total images copied : {total_copied}")
print(f"  Test folder         : {DEST_TEST}")
print("=" * 60)
print("Done! Re-run Test_Model_Performance.ipynb to generate results.")
