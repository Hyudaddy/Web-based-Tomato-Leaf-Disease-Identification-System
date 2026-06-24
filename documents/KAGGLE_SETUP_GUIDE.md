# Kaggle Dataset Download Guide

## Quick Setup (5 minutes)

### Step 1: Install Kaggle CLI
```bash
pip install kaggle
```

### Step 2: Get Kaggle API Key
1. Go to: https://www.kaggle.com/settings/account
2. Click "Create New API Token"
3. A file `kaggle.json` will download
4. Move it to: `C:\Users\HYUDADDY\.kaggle\`

**Create the folder if it doesn't exist:**
```bash
mkdir C:\Users\HYUDADDY\.kaggle
```

### Step 3: Run the Download Script
```bash
python download_from_kaggle.py
```

This will:
1. Download the dataset (~500MB, takes 5-10 mins)
2. Extract images
3. Split into training (70%) and validation (30%)
4. Organize into your Unidentified folders
5. Clean up temporary files

---

## What You'll Get

From the Kaggle dataset:
- **~1000+ random images** of various objects, scenes, people, etc.
- Perfect for teaching the model what's NOT a tomato leaf
- Automatically split: 70% training, 30% validation

---

## After Download

Once the script completes, run:
```bash
python retrain_model_with_unidentified.py
```

This will fine-tune your model with the new Unidentified class.

---

## Troubleshooting

### "kaggle: command not found"
- Make sure you installed: `pip install kaggle`
- Restart your terminal/IDE

### "403 - Unauthorized"
- Check that `kaggle.json` is in the right place
- Verify your API key is valid

### "Dataset not found"
- Make sure the dataset URL is correct
- Check your internet connection

---

## Dataset Source
https://www.kaggle.com/datasets/pankajkumar2002/random-image-sample-dataset

Great choice! This dataset has diverse images perfect for the Unidentified class. 🎯
