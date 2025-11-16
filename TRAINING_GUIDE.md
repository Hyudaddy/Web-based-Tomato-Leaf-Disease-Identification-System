# 🌱 Tomato Leaf Disease Detection - Model Retraining Guide

## Overview
This guide will help you retrain your model with the full dataset to improve accuracy on low-quality images.

---

## 📋 Your Configuration

| Setting | Value |
|---------|-------|
| **Option** | C (Balanced) |
| **Device** | CPU (Intel Core i3) |
| **Image Size** | 192x192 |
| **Batch Size** | 20 |
| **Epochs** | 35 (with early stopping) |
| **Learning Rate** | 0.0005 |
| **Estimated Time** | 30-60 minutes |

---

## 🚀 Step-by-Step Instructions

### Step 1: Analyze Your Dataset (5 minutes)

Before training, check your dataset distribution:

```bash
python analyze_dataset.py
```

**What to look for:**
- ✅ All 11 classes are present
- ✅ Each class has at least 50-100 images
- ✅ Classes are relatively balanced (not >3x difference)

**Example output:**
```
Training samples: 5000
Validation samples: 1500
Classes: 11
Balance ratio: 1.5x (good!)
```

---

### Step 2: Backup Your Current Model (2 minutes)

Before training, backup your existing model:

```bash
# Copy current model
cp C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito.h5 `
   C:\Users\HYUDADDY\Desktop\TLDI_system\backend\trained_model_fito_backup.h5
```

---

### Step 3: Start Training (30-60 minutes)

Run the optimized training script:

```bash
python train_model_optimized.py
```

**What happens during training:**
- Loads full dataset with enhanced augmentation
- Trains for up to 35 epochs
- Saves best model automatically
- Stops early if no improvement (prevents overfitting)
- Reduces learning rate if stuck on plateau

**You'll see output like:**
```
Epoch 1/35
1000/1000 [==============================] - 120s - loss: 0.8234 - accuracy: 0.7234 - val_loss: 0.6234 - val_accuracy: 0.8123
Epoch 2/35
...
```

---

### Step 4: Monitor Training Progress

**Good signs:**
- ✅ Validation accuracy increases over epochs
- ✅ Training loss decreases
- ✅ No huge jumps in loss (stable training)

**Warning signs:**
- ❌ Validation accuracy plateaus early
- ❌ Training loss increases (learning rate too high)
- ❌ Validation loss increases while training loss decreases (overfitting)

---

### Step 5: After Training Completes

The script will show:
```
Final Validation Accuracy: 92.34%
Final Validation Loss: 0.2456
```

**Check the training history:**
```bash
# View the JSON file with detailed metrics
type training_history.json
```

---

### Step 6: Test the New Model

1. **Restart your backend API** to load the new model
2. **Test with low-quality images:**
   - Blurry photos
   - Poor lighting
   - Partial leaf visibility
   - Different angles

3. **Compare with old model:**
   - Does it identify more images correctly?
   - Fewer "cannot identify" results?

---

## 🔧 Key Improvements in This Training

### 1. Enhanced Data Augmentation
```python
brightness_range=[0.7, 1.3]  # Handles dim/bright images
rotation_range=25             # More rotation variations
vertical_flip=True            # Additional leaf orientations
```

**Why:** Helps model learn diseases in various lighting and angles

### 2. Larger Image Size (192x192)
- **Before:** 128x128 (small, loses detail)
- **After:** 192x192 (better feature extraction)
- **Trade-off:** Slightly slower but better accuracy

### 3. Smaller Batch Size (20)
- **Before:** 32
- **After:** 20
- **Why:** More gradient updates per epoch, better for CPU

### 4. Lower Learning Rate (0.0005)
- **Before:** 0.001
- **After:** 0.0005
- **Why:** More careful learning, better convergence

### 5. Early Stopping
- Stops training if validation loss doesn't improve for 5 epochs
- Prevents overfitting
- Saves training time

### 6. Learning Rate Reduction
- Automatically reduces learning rate if stuck
- Helps escape local minima

---

## 📊 Expected Results

### Before Retraining
- Accuracy: ~85%
- Issues: Cannot identify low-quality images
- False negatives: High

### After Retraining (Expected)
- Accuracy: 88-92%
- Issues: Better handling of low-quality images
- False negatives: Reduced

**Note:** Exact improvement depends on dataset quality and balance

---

## ⚠️ Troubleshooting

### Problem: Training is very slow
**Solution:**
- This is normal on CPU (Intel Core i3)
- Reduce BATCH_SIZE to 16 in the script
- Or increase to 24 if you have more RAM

### Problem: Out of memory error
**Solution:**
- Reduce BATCH_SIZE from 20 to 16
- Reduce IMG_SIZE from 192 to 160

### Problem: Model accuracy didn't improve
**Possible causes:**
- Dataset is imbalanced (check analyze_dataset.py output)
- Dataset is too small (<1000 images total)
- Low-quality images in dataset
- Solution: Collect more high-quality training data

### Problem: Model still says "cannot identify"
**Possible causes:**
- Confidence threshold too high (check backend/model_handler.py)
- Image quality still too poor
- Class not well-represented in training data
- Solution: Lower confidence threshold or add more training data for that class

---

## 🎯 Tips for Best Results

1. **Dataset Quality**
   - Ensure training images are actual tomato leaves
   - Remove corrupted or irrelevant images
   - Include diverse lighting conditions

2. **Testing**
   - Test with various image qualities
   - Test with different angles and distances
   - Test with both diseased and healthy leaves

3. **Iteration**
   - If accuracy is still low, collect more data
   - Focus on classes with low accuracy
   - Retrain with additional data

4. **Monitoring**
   - Check training_history.json after each training
   - Compare with previous runs
   - Track accuracy improvements

---

## 📁 Files Created/Modified

| File | Purpose |
|------|---------|
| `train_model_optimized.py` | Main training script (Option C) |
| `analyze_dataset.py` | Dataset analysis tool |
| `training_history.json` | Training metrics (created after training) |
| `backend/trained_model_fito.h5` | New trained model |
| `backend/trained_model_fito_backup.h5` | Backup of old model |

---

## 🔄 Retraining Workflow

```
1. Run analyze_dataset.py
   ↓
2. Backup current model
   ↓
3. Run train_model_optimized.py (30-60 min)
   ↓
4. Check training_history.json
   ↓
5. Restart backend API
   ↓
6. Test with low-quality images
   ↓
7. If satisfied, keep new model
   If not, adjust and retrain
```

---

## 📞 Quick Reference

**Analyze dataset:**
```bash
python analyze_dataset.py
```

**Start training:**
```bash
python train_model_optimized.py
```

**Check history:**
```bash
type training_history.json
```

**Backup model:**
```bash
copy backend\trained_model_fito.h5 backend\trained_model_fito_backup.h5
```

---

## ✅ Checklist Before Training

- [ ] Dataset analyzed (all 11 classes present)
- [ ] Current model backed up
- [ ] Enough disk space (~500MB for model)
- [ ] No other heavy processes running
- [ ] Terminal/PowerShell ready
- [ ] Time available (30-60 minutes)

---

## 🎓 Understanding the Output

### Training Output Example
```
Epoch 1/35
1000/1000 [==============================] - 120s - loss: 0.8234 - accuracy: 0.7234 - val_loss: 0.6234 - val_accuracy: 0.8123
```

**Breakdown:**
- `1000/1000` - 1000 batches processed
- `loss: 0.8234` - Training loss (lower is better)
- `accuracy: 0.7234` - Training accuracy (higher is better)
- `val_loss: 0.6234` - Validation loss
- `val_accuracy: 0.8123` - Validation accuracy (target metric)

**Good training:**
- Validation accuracy increases
- Validation loss decreases
- No sudden spikes

---

## 🚀 Next Steps After Training

1. **Deploy new model**
   - Restart backend API
   - Verify model loads correctly

2. **Test thoroughly**
   - Test with low-quality images
   - Test with different diseases
   - Test with healthy leaves

3. **Monitor in production**
   - Track user feedback
   - Monitor accuracy metrics
   - Collect misclassified images for future retraining

4. **Plan future improvements**
   - Collect more data if needed
   - Retrain quarterly with new data
   - Consider fine-tuning with user feedback

---

**Good luck with your retraining! 🌱**
