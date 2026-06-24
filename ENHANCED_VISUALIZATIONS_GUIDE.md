# Enhanced Visualizations - Usage Guide

## Overview
This script generates advanced model evaluation visualizations with a clean blue color palette suitable for documentation.

## Features
✅ **ROC Curves** - One-vs-Rest with AUC scores  
✅ **Precision-Recall Curves** - Per-class with Average Precision  
✅ **Calibration Plot** - Reliability diagram with Brier score  
✅ **Top-K Accuracy** - Shows top-1 through top-5 accuracy  
✅ **Error Analysis Matrix** - Identifies most common misclassifications  
✅ **Confidence vs Correctness** - Analyzes prediction confidence reliability  

## Setup

### 1. Update Configuration
Edit `enhanced_visualizations.py` and update the `DATASET_PATH` variable:

```python
DATASET_PATH = r"C:\Path\To\Your\Dataset"
```

The dataset should have this structure:
```
dataset/
├── validation/
│   ├── Bacterial Spot/
│   ├── Early Blight/
│   ├── Late Blight/
│   ├── Leaf Mold/
│   ├── Septoria Leaf Spot/
│   ├── Spider Mites/
│   ├── Target Spot/
│   ├── Yellow Leaf Curl Virus/
│   ├── Mosaic Virus/
│   ├── Healthy/
│   └── Unidentified/  (will be excluded from analysis)
```

### 2. Install Dependencies
```bash
pip install numpy matplotlib seaborn scikit-learn tensorflow
```

### 3. Run the Script
```bash
python enhanced_visualizations.py
```

## Output Files

All visualizations are saved to the `enhanced_visualizations/` directory:

1. **1_roc_curves.png** - ROC curves for all classes with AUC scores
2. **2_precision_recall_curves.png** - PR curves with Average Precision scores
3. **3_calibration_plot.png** - Reliability diagram showing model calibration
4. **4_topk_accuracy.png** - Bar chart of top-1 through top-5 accuracy
5. **5_error_analysis_matrix.png** - Heatmap of misclassifications
6. **6_confidence_vs_correctness.png** - Confidence analysis with sample distribution
7. **summary_report.txt** - Text summary of all metrics

## Color Palette

All visualizations use a professional blue color scheme:
- **Primary Blue**: `#2E5EAA` (Deep blue)
- **Secondary Blue**: `#4A90E2` (Medium blue)
- **Light Blue**: `#7FB3D5` (Highlights)
- **Accent Blue**: `#1E3A5F` (Dark accents)

## Notes

- The **Unidentified** class is automatically excluded from all analyses
- All plots are saved at **300 DPI** for publication quality
- The script requires the trained model and training history JSON file
- Validation data should not be shuffled (the script handles this)

## Interpreting Results

### ROC Curves
- **AUC = 1.0**: Perfect classifier
- **AUC = 0.5**: Random classifier
- **AUC > 0.8**: Good performance

### Precision-Recall Curves
- Better than ROC for imbalanced datasets
- **AP (Average Precision)**: Area under the PR curve
- Higher AP = better performance

### Calibration Plot
- Points on diagonal = well-calibrated
- Above diagonal = overconfident
- Below diagonal = underconfident
- **Brier Score**: Lower is better (0 = perfect)

### Top-K Accuracy
- Shows if true class is in top K predictions
- Useful for understanding model uncertainty
- Large gap between top-1 and top-3 suggests confusion

### Error Analysis
- Shows which disease pairs are most confused
- Helps identify areas for model improvement
- Can guide data collection efforts

## Troubleshooting

**Error: "No module named 'tensorflow'"**
```bash
pip install tensorflow
```

**Error: "Cannot find path"**
- Check that `DATASET_PATH` is correct
- Ensure validation folder exists
- Use raw string (r"path") for Windows paths

**Error: "Unidentified class not found"**
- This is normal if your dataset doesn't have an Unidentified class
- The script will proceed without filtering

## Contact
For issues or questions, refer to the main project documentation.
