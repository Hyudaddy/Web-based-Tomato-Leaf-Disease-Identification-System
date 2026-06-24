# Quick Reference: Table 16 for Thesis

## What is Table 16?

Table 16 is the **Performance Evaluation of the Classification** table that shows how well your Fito model performs on each tomato disease class.

---

## How to Generate Table 16

### Step 1: Run the Evaluation Script

```bash
cd C:\Users\HYUDADDY\Desktop\TLDI_system
python scripts\generate_performance_table.py
```

### Step 2: Wait for Completion

The script will:
- Load your trained model
- Process all validation images (~5,488 images)
- Calculate metrics for each class
- Generate the table

**Expected time:** 5-10 minutes (depending on your CPU)

### Step 3: Copy the Results

The script will output:
1. **Console output** - Formatted table you can copy
2. **JSON file** - `performance_evaluation_results.json` with all data
3. **Markdown table** - Ready to paste into your thesis

---

## Understanding the Metrics

### For Each Disease Class:

| Metric | What it Means | Good Value |
|--------|---------------|------------|
| **Accuracy** | How often the model is correct for this disease | ≥ 0.85 |
| **Precision** | When model says "this disease", how often is it right? | ≥ 0.80 |
| **Recall** | Of all actual cases of this disease, how many did we catch? | ≥ 0.80 |
| **F1-Score** | Balanced measure of precision and recall | ≥ 0.80 |

### Example Interpretation:

**Bacterial Spot: Accuracy=0.92, Precision=0.89, Recall=0.91, F1=0.90**

This means:
- ✅ 92% of Bacterial Spot images are correctly classified
- ✅ When the model says "Bacterial Spot", it's right 89% of the time
- ✅ The model catches 91% of all actual Bacterial Spot cases
- ✅ Overall balanced performance: 90% (F1-Score)

---

## Table 16 Template for Your Thesis

Copy this structure and fill in with your generated values:

```markdown
### Table 16. Performance Evaluation of the Classification

| Tomato Disease | Number of Test Images | Accuracy | Precision | Recall | F1-Score |
|----------------|----------------------|----------|-----------|--------|----------|
| Bacterial Spot | 500 | 0.92 | 0.89 | 0.91 | 0.90 |
| Early Blight | 520 | 0.88 | 0.85 | 0.87 | 0.86 |
| Late Blight | 510 | 0.90 | 0.88 | 0.89 | 0.88 |
| Leaf Mold | 495 | 0.87 | 0.84 | 0.86 | 0.85 |
| Septoria Leaf Spot | 505 | 0.89 | 0.86 | 0.88 | 0.87 |
| Spider Mites | 480 | 0.91 | 0.89 | 0.90 | 0.89 |
| Target Spot | 490 | 0.88 | 0.85 | 0.87 | 0.86 |
| Yellow Leaf Curl Virus | 500 | 0.90 | 0.87 | 0.89 | 0.88 |
| Mosaic Virus | 498 | 0.89 | 0.86 | 0.88 | 0.87 |
| Healthy | 510 | 0.93 | 0.91 | 0.92 | 0.91 |
| Unidentified | 480 | 0.85 | 0.82 | 0.84 | 0.83 |
| **TOTAL** | **5,488** | **HIGH** | **HIGH** | **HIGH** | **HIGH** |

**Overall Model Accuracy:** 0.9005 (90.05%)
```

---

## What to Write in Your Discussion

### Sample Text for Chapter 4:

> "Table 16 shows the model's performance evaluated with different test images from the validation dataset. The metrics used to estimate the model's performance are **precision**, **recall**, **accuracy**, and **F1-score**. A confusion matrix was constructed to measure the model's performance, which is a table outline representing the efficiency of the model and its performance.
>
> The Fito system achieved an overall accuracy of **90.05%** across all 11 classes, demonstrating excellent classification capability. The model showed particularly strong performance in identifying **Healthy** leaves (93% accuracy) and **Bacterial Spot** (92% accuracy), while maintaining consistent performance across other disease classes.
>
> **Precision** values ranged from 0.82 to 0.91, indicating that when the model predicts a specific disease, it is correct approximately 82-91% of the time. **Recall** values ranged from 0.84 to 0.92, showing that the model successfully identifies 84-92% of actual disease cases. The **F1-scores** (0.83-0.91) demonstrate balanced performance between precision and recall across all classes.
>
> These results indicate that the Fito system is suitable for practical deployment in agricultural settings, providing reliable disease identification to support farmer decision-making."

---

## Formulas to Include

Include these formulas in your thesis before Table 16:

### Accuracy
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

### Precision
```
Precision = TP / (TP + FP)
```

### Recall
```
Recall = TP / (TP + FN)
```

### F1-Score
```
F1-Score = 2 × (Precision × Recall) / (Precision + Recall)
```

Where:
- **TP** (True Positive): Correctly predicted as the disease
- **TN** (True Negative): Correctly predicted as NOT the disease
- **FP** (False Positive): Incorrectly predicted as the disease
- **FN** (False Negative): Incorrectly predicted as NOT the disease

---

## Confusion Matrix Explanation

Include this text:

> "A confusion matrix is constructed to measure the model's performance. It is a table outline representing the efficiency of the model and its performance. The confusion matrix displays the number of correct and incorrect predictions made by the model, organized by class. The diagonal elements represent correct predictions, while off-diagonal elements represent misclassifications."

---

## Files Generated

After running the script, you'll have:

1. **`performance_evaluation_results.json`**
   - Complete numerical results
   - Machine-readable format
   - Backup of all metrics

2. **Console Output**
   - Formatted table
   - Markdown version
   - Confusion matrix summary

3. **`documents/PERFORMANCE_EVALUATION_DOCUMENTATION.md`**
   - Complete documentation
   - Formulas and explanations
   - Analysis guidelines

---

## Troubleshooting

### Script Not Running?

**Error: "Validation data not found"**
- Update the path in `generate_performance_table.py` line 23
- Point to your actual validation dataset location

**Error: "Model not found"**
- Ensure `backend/trained_model_fito.h5` exists
- Check if you've trained the model

**Taking too long?**
- Normal! Processing 5,000+ images takes time
- Wait 5-10 minutes for completion
- Don't interrupt the process

### Need Different Format?

The script outputs:
- Plain text table (for viewing)
- Markdown table (for documents)
- JSON data (for further processing)

Choose the format that works best for your thesis!

---

## Quick Checklist

- [ ] Run `python scripts\generate_performance_table.py`
- [ ] Wait for script to complete (~5-10 minutes)
- [ ] Copy the markdown table from console output
- [ ] Paste into your thesis at Table 16 location
- [ ] Add formulas before the table
- [ ] Write interpretation after the table
- [ ] Save `performance_evaluation_results.json` for reference
- [ ] Include confusion matrix discussion if needed

---

**Ready to generate your Table 16?**

```bash
python scripts\generate_performance_table.py
```

Good luck with your thesis! 🎓🍅
