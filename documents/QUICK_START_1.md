# ⚡ Quick Start - Model Retraining

## 🎯 Your Setup
- **Option:** C (Balanced)
- **Device:** Intel Core i3 (CPU)
- **Time:** 30-60 minutes
- **Goal:** Better accuracy on low-quality images

---

## 🚀 Three Simple Steps

### Step 1: Check Everything (5 min)
```bash
python check_and_prepare.py
```
**Expected output:** `✅ ALL CHECKS PASSED! Ready to train!`

---

### Step 2: Analyze Dataset (5 min)
```bash
python analyze_dataset.py
```
**What to look for:**
- All 11 classes present
- Each class has images
- Balanced distribution

---

### Step 3: Train Model (30-60 min)
```bash
python train_model_optimized.py
```

**What happens:**
- Loads full dataset
- Trains for up to 35 epochs
- Saves best model automatically
- Shows progress each epoch

**Expected final output:**
```
✅ Final Validation Accuracy: 88-92%
✅ New model saved at: C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito.h5
```

---

## ✅ After Training

1. **Restart your backend API**
2. **Test with low-quality images**
3. **Check if "cannot identify" results decreased**

---

## 📊 What's Different

| Aspect | Before | After |
|--------|--------|-------|
| Image Size | 128x128 | 192x192 |
| Batch Size | 32 | 20 |
| Epochs | 20 | 35 |
| Learning Rate | 0.001 | 0.0005 |
| Augmentation | Basic | Enhanced (brightness, contrast) |

---

## 💡 Key Improvements

✅ Handles low-quality images better  
✅ Better feature extraction (larger images)  
✅ More training iterations (35 epochs)  
✅ Brightness/contrast adjustments for poor lighting  
✅ Early stopping prevents overfitting  

---

## ⚠️ If Something Goes Wrong

**Slow training?**
- Normal on CPU - just wait
- Or reduce BATCH_SIZE to 16 in script

**Out of memory?**
- Reduce BATCH_SIZE to 16
- Or reduce IMG_SIZE to 160

**Accuracy didn't improve?**
- Check dataset balance: `python analyze_dataset.py`
- Might need more training data

---

## 📁 Files

- `train_model_optimized.py` ← Main script
- `analyze_dataset.py` ← Check dataset
- `check_and_prepare.py` ← Pre-flight check
- `TRAINING_GUIDE.md` ← Detailed guide
- `training_history.json` ← Results (after training)

---

## 🎓 Understanding Progress

```
Epoch 1/35
1000/1000 [==============================] - 120s - loss: 0.8234 - accuracy: 0.7234 - val_loss: 0.6234 - val_accuracy: 0.8123
```

**Good signs:**
- ✅ val_accuracy increases each epoch
- ✅ val_loss decreases
- ✅ No sudden jumps

**Bad signs:**
- ❌ val_accuracy stays same
- ❌ val_loss increases
- ❌ Training crashes

---

## 🔄 Workflow

```
Run check_and_prepare.py
         ↓
Run analyze_dataset.py
         ↓
Run train_model_optimized.py (30-60 min)
         ↓
Check training_history.json
         ↓
Restart backend API
         ↓
Test with low-quality images
```

---

**Ready? Let's go! 🚀**

```bash
python check_and_prepare.py
```
