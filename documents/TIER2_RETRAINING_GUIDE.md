# Tier 2: Model Retraining with Unidentified Class

## Overview
This guide walks you through retraining your model to explicitly recognize and reject non-tomato images by adding an "Unidentified" class.

## Why Tier 2?
- **Tier 1** (confidence threshold) catches some non-tomato images but isn't perfect
- **Tier 2** teaches the model to explicitly recognize what's NOT a tomato leaf
- Result: Much more accurate rejection of non-tomato images

## What You'll Do

### Step 1: Download Non-Tomato Images ⬇️
Run this script to automatically download ~400 diverse non-tomato images:

```bash
python download_unidentified_images.py
```

**What it downloads:**
- Human faces and portraits
- Random objects
- Other plants and flowers
- Landscapes and nature
- Food items
- Buildings and architecture
- And more...

**Expected output:**
- ~280 images in `training/Unidentified/`
- ~120 images in `validation/Unidentified/`

**Time:** ~5-10 minutes (depends on internet speed)

### Step 2: Review Downloaded Images (Optional)
Open the folders to make sure images look good:
- `C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\training\Unidentified\`
- `C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation\Unidentified\`

You can delete any images that look wrong.

### Step 3: Retrain the Model 🔄
Run this script to fine-tune your model with the new class:

```bash
python retrain_model_with_unidentified.py
```

**What it does:**
1. Loads your existing trained model
2. Adds the new "Unidentified" class (now 11 classes total)
3. Fine-tunes for 8 epochs (fast!)
4. Saves as `trained_model_fito_v2.h5`

**Expected time:** 10-20 minutes (depends on your GPU)

### Step 4: Replace the Old Model 🔄
Once retraining completes:

```bash
# Backup the old model
copy C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito.h5 C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito.h5.backup

# Replace with new model
copy C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito_v2.h5 C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito.h5
```

### Step 5: Restart Backend & Test 🧪
1. Kill the old backend process
2. Start the backend again:
   ```bash
   python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
3. Upload your face image - it should now be rejected as "Unidentified"
4. Upload a real tomato leaf - it should work normally

## Model Classes After Retraining

Your model will now recognize 11 classes:

```
0: Bacterial Spot
1: Early Blight
2: Late Blight
3: Leaf Mold
4: Septoria Leaf Spot
5: Spider Mites
6: Target Spot
7: Yellow Leaf Curl Virus
8: Mosaic Virus
9: Healthy
10: Unidentified ← NEW!
```

## Troubleshooting

### Issue: Download script fails
- Check your internet connection
- Try running again - sometimes Bing blocks requests
- Alternatively, manually download images from Google Images and place in the folders

### Issue: Retraining is very slow
- This is normal if you don't have a GPU
- It will still complete, just takes longer
- You can reduce `EPOCHS` in the script if needed

### Issue: Model still predicts diseases for non-tomato images
- The model might need more non-tomato images
- Try collecting 500-1000 more images
- Or increase `EPOCHS` to 10-15 for more training

## Advanced: Manual Image Collection

If the download script doesn't work well, you can manually collect images:

1. Take 50-100 selfies from different angles
2. Download ~200-300 images from Google Images:
   - Search: "random objects", "faces", "plants", "flowers", "landscapes"
   - Save to `training/Unidentified/` and `validation/Unidentified/`
3. Split: 70% training, 30% validation

## What's Next?

After successful retraining:
- Your model will be much more robust
- Non-tomato images will be reliably rejected
- You can deploy with confidence!

## Questions?

If something goes wrong:
1. Check the console output for error messages
2. Make sure all image files are valid (JPEG/PNG)
3. Ensure you have enough disk space (~2GB)
4. Try restarting and running again

---

**Good luck! 🍅🚀**
