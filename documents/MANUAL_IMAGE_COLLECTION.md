# Manual Image Collection for Unidentified Class

Since automatic downloading is having issues, here's the easiest way to collect images:

## Option 1: Use Your Own Photos (Fastest ⚡)

### Step 1: Collect Your Face Images
1. Take 50-100 selfies with your phone/camera from different angles:
   - Front facing
   - Side angles
   - Different lighting (bright, dim, natural light)
   - Different backgrounds
   - Different expressions

2. Save them to: `C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\training\Unidentified\`

### Step 2: Collect Other Objects
Take photos of random objects around your house:
- Your desk/workspace
- Food items (apple, orange, bread, etc.)
- Books and papers
- Flowers or other plants
- Your pets
- Outdoor scenes
- Buildings
- Trees

Aim for 200-300 total photos.

### Step 3: Split Into Training/Validation
- Count your photos
- Move 70% to `training/Unidentified/`
- Move 30% to `validation/Unidentified/`

**Example:**
- 280 photos total
- 196 to training folder (70%)
- 84 to validation folder (30%)

---

## Option 2: Download from Google Images (Easy 📥)

### Step 1: Open Google Images
Go to: https://images.google.com/

### Step 2: Search for diverse images
Search for each of these and download 20-30 images per search:
- "human face"
- "random objects"
- "flowers"
- "food items"
- "buildings"
- "landscapes"
- "animals"
- "plants"
- "outdoor scenes"
- "indoor objects"

### Step 3: Organize
- Save all images to a temp folder
- Rename them to something simple (image_001.jpg, image_002.jpg, etc.)
- Move 70% to training folder
- Move 30% to validation folder

---

## Option 3: Use Stock Photos (Professional 🎨)

Free stock photo sites:
- **Unsplash**: https://unsplash.com/ (download bulk)
- **Pexels**: https://www.pexels.com/ (free photos)
- **Pixabay**: https://pixabay.com/ (free images)

Search for "random objects", "faces", "nature", etc. and download 200-300 images.

---

## Folder Structure After Collection

```
C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\
├── training\
│   ├── Unidentified\
│   │   ├── image_001.jpg
│   │   ├── image_002.jpg
│   │   ├── ... (196 images)
│   │   └── image_196.jpg
│   └── ... (other disease folders)
└── validation\
    ├── Unidentified\
    │   ├── image_001.jpg
    │   ├── image_002.jpg
    │   ├── ... (84 images)
    │   └── image_084.jpg
    └── ... (other disease folders)
```

---

## Quick Check

Before running retraining, verify:
```bash
# Count training images
dir "C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\training\Unidentified" /s

# Count validation images
dir "C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation\Unidentified" /s
```

You should have:
- ✅ At least 150-200 training images
- ✅ At least 50-100 validation images
- ✅ Mix of faces, objects, plants, landscapes, etc.

---

## Next Steps

Once you have collected images:
1. Verify folder counts
2. Run: `python retrain_model_with_unidentified.py`
3. Wait 10-20 minutes for retraining
4. Test with your face!

---

**Recommended:** Use Option 1 (your own photos) - it's fastest and most effective! 📸
