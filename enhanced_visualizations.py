#!/usr/bin/env python3
"""
================================================================================
ENHANCED MODEL EVALUATION VISUALIZATIONS
================================================================================
This script generates advanced visualizations for model evaluation including:
- ROC Curves (One-vs-Rest)
- Precision-Recall Curves
- Calibration Plot
- Top-K Accuracy
- Error Analysis Matrix

Features:
- Clean blue color palette for documentation
- Excludes "Unidentified" class from analysis
- High-resolution outputs suitable for publication

Usage:
    Update the configuration paths below and run the script.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve, average_precision_score,
    confusion_matrix, top_k_accuracy_score, calibration_curve
)
from sklearn.preprocessing import label_binarize
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from datetime import datetime

# ================================================================================
# CONFIGURATION - Update these paths to match your setup
# ================================================================================
# Get the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Model and history paths (relative to script directory)
MODEL_PATH = os.path.join(SCRIPT_DIR, "backend", "trained_model_fito.h5")
HISTORY_PATH = os.path.join(SCRIPT_DIR, "training_history.json")

# Dataset path - UPDATE THIS to point to your validation dataset
# Example: r"C:\Users\YourName\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
DATASET_PATH = r"UPDATE_THIS_PATH"  # ⚠️ UPDATE THIS!
VAL_PATH = os.path.join(DATASET_PATH, "validation")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "enhanced_visualizations")


IMG_SIZE = 224
BATCH_SIZE = 32

# Blue color palette for clean documentation
BLUE_PALETTE = {
    'primary': '#2E5EAA',      # Deep blue
    'secondary': '#4A90E2',    # Medium blue
    'light': '#7FB3D5',        # Light blue
    'accent': '#1E3A5F',       # Dark blue
    'gradient': ['#E8F4F8', '#D0E8F2', '#B8DCEC', '#A0D0E6', '#88C4E0', '#70B8DA']
}

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set matplotlib style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.2)

print("=" * 80)
print("ENHANCED MODEL EVALUATION VISUALIZATIONS")
print("=" * 80)
print(f"\n📁 Configuration:")
print(f"   • Model: {MODEL_PATH}")
print(f"   • Output Directory: {OUTPUT_DIR}")

# ================================================================================
# LOAD MODEL AND DATA
# ================================================================================
print("\n" + "=" * 80)
print("STEP 1: Loading model and data...")
print("=" * 80)

# Load trained model
model = load_model(MODEL_PATH)
print(f"✓ Model loaded: {model.count_params():,} parameters")

# Load validation data
val_datagen = ImageDataGenerator(rescale=1./255)
val_generator = val_datagen.flow_from_directory(
    VAL_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# Get class names and exclude "Unidentified"
all_class_names = list(val_generator.class_indices.keys())
print(f"\n📋 All classes found: {all_class_names}")

# Filter out "Unidentified" class
if "Unidentified" in all_class_names:
    unidentified_idx = all_class_names.index("Unidentified")
    class_names = [c for c in all_class_names if c != "Unidentified"]
    print(f"✓ Excluding 'Unidentified' class from analysis")
else:
    class_names = all_class_names
    unidentified_idx = None

num_classes = len(class_names)
print(f"✓ Analyzing {num_classes} disease classes")

# Get predictions
print("\n🔄 Generating predictions...")
y_pred_probs = model.predict(val_generator, verbose=1)
y_true = val_generator.classes

# Filter out unidentified class samples if present
if unidentified_idx is not None:
    # Keep only samples that are NOT from the unidentified class
    mask = y_true != unidentified_idx
    y_true_filtered = y_true[mask]
    y_pred_probs_filtered = y_pred_probs[mask]
    
    # Remove unidentified column from predictions
    y_pred_probs_filtered = np.delete(y_pred_probs_filtered, unidentified_idx, axis=1)
    
    # Adjust class indices (shift down if necessary)
    y_true_filtered = np.array([idx if idx < unidentified_idx else idx - 1 for idx in y_true_filtered])
else:
    y_true_filtered = y_true
    y_pred_probs_filtered = y_pred_probs

y_pred_filtered = np.argmax(y_pred_probs_filtered, axis=1)

print(f"✓ Filtered dataset: {len(y_true_filtered)} samples across {num_classes} classes")

# ================================================================================
# VISUALIZATION 1: ROC Curves (One-vs-Rest)
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 1: ROC Curves (One-vs-Rest)")
print("=" * 80)

# Binarize the labels for one-vs-rest
y_true_bin = label_binarize(y_true_filtered, classes=range(num_classes))

# Compute ROC curve and AUC for each class
fpr = dict()
tpr = dict()
roc_auc = dict()

for i in range(num_classes):
    fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_pred_probs_filtered[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and AUC
fpr["micro"], tpr["micro"], _ = roc_curve(y_true_bin.ravel(), y_pred_probs_filtered.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

# Plot ROC curves
fig, ax = plt.subplots(figsize=(12, 10))

# Plot micro-average
ax.plot(fpr["micro"], tpr["micro"],
        label=f'Micro-average (AUC = {roc_auc["micro"]:.3f})',
        color=BLUE_PALETTE['accent'], linestyle='--', linewidth=3)

# Plot per-class ROC curves with blue gradient
colors = sns.color_palette("Blues_d", num_classes)
for i, color in enumerate(colors):
    ax.plot(fpr[i], tpr[i], color=color, linewidth=2,
            label=f'{class_names[i]} (AUC = {roc_auc[i]:.3f})')

# Plot diagonal reference line
ax.plot([0, 1], [0, 1], 'k--', linewidth=1, alpha=0.3, label='Random Classifier')

ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('False Positive Rate', fontsize=13, fontweight='bold')
ax.set_ylabel('True Positive Rate', fontsize=13, fontweight='bold')
ax.set_title('ROC Curves - One-vs-Rest (Multi-Class)', fontsize=15, fontweight='bold')
ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '1_roc_curves.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# VISUALIZATION 2: Precision-Recall Curves
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 2: Precision-Recall Curves")
print("=" * 80)

# Compute Precision-Recall curve and average precision for each class
precision = dict()
recall = dict()
avg_precision = dict()

for i in range(num_classes):
    precision[i], recall[i], _ = precision_recall_curve(y_true_bin[:, i], y_pred_probs_filtered[:, i])
    avg_precision[i] = average_precision_score(y_true_bin[:, i], y_pred_probs_filtered[:, i])

# Compute micro-average
precision["micro"], recall["micro"], _ = precision_recall_curve(
    y_true_bin.ravel(), y_pred_probs_filtered.ravel()
)
avg_precision["micro"] = average_precision_score(y_true_bin, y_pred_probs_filtered, average="micro")

# Plot Precision-Recall curves
fig, ax = plt.subplots(figsize=(12, 10))

# Plot micro-average
ax.plot(recall["micro"], precision["micro"],
        label=f'Micro-average (AP = {avg_precision["micro"]:.3f})',
        color=BLUE_PALETTE['accent'], linestyle='--', linewidth=3)

# Plot per-class curves with blue gradient
colors = sns.color_palette("Blues_d", num_classes)
for i, color in enumerate(colors):
    ax.plot(recall[i], precision[i], color=color, linewidth=2,
            label=f'{class_names[i]} (AP = {avg_precision[i]:.3f})')

ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('Recall', fontsize=13, fontweight='bold')
ax.set_ylabel('Precision', fontsize=13, fontweight='bold')
ax.set_title('Precision-Recall Curves (Multi-Class)', fontsize=15, fontweight='bold')
ax.legend(loc="lower left", fontsize=9, framealpha=0.9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '2_precision_recall_curves.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# VISUALIZATION 3: Calibration Plot
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 3: Calibration Plot")
print("=" * 80)

# Get predicted probabilities for the predicted class
y_pred_max_probs = np.max(y_pred_probs_filtered, axis=1)

# Compute calibration curve
fraction_of_positives, mean_predicted_value = calibration_curve(
    y_true_filtered == y_pred_filtered,  # Binary: correct or not
    y_pred_max_probs,
    n_bins=10,
    strategy='uniform'
)

# Plot calibration curve
fig, ax = plt.subplots(figsize=(10, 10))

# Plot perfect calibration line
ax.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Perfectly Calibrated', alpha=0.5)

# Plot model calibration
ax.plot(mean_predicted_value, fraction_of_positives, 
        marker='o', linewidth=3, markersize=10,
        color=BLUE_PALETTE['primary'], label='Model Calibration')

# Fill area between perfect and actual
ax.fill_between(mean_predicted_value, fraction_of_positives, mean_predicted_value,
                alpha=0.2, color=BLUE_PALETTE['light'])

ax.set_xlabel('Mean Predicted Probability', fontsize=13, fontweight='bold')
ax.set_ylabel('Fraction of Positives', fontsize=13, fontweight='bold')
ax.set_title('Calibration Plot (Reliability Diagram)', fontsize=15, fontweight='bold')
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.0])

# Add text box with calibration statistics
from sklearn.metrics import brier_score_loss
brier_score = brier_score_loss(y_true_filtered == y_pred_filtered, y_pred_max_probs)
textstr = f'Brier Score: {brier_score:.4f}\n(Lower is better)'
props = dict(boxstyle='round', facecolor=BLUE_PALETTE['light'], alpha=0.3)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=props)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '3_calibration_plot.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# VISUALIZATION 4: Top-K Accuracy
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 4: Top-K Accuracy")
print("=" * 80)

# Calculate top-k accuracy for k=1 to 5
k_values = range(1, min(6, num_classes + 1))
top_k_accuracies = []

for k in k_values:
    top_k_acc = top_k_accuracy_score(y_true_filtered, y_pred_probs_filtered, k=k)
    top_k_accuracies.append(top_k_acc * 100)
    print(f"   Top-{k} Accuracy: {top_k_acc * 100:.2f}%")

# Plot Top-K accuracy
fig, ax = plt.subplots(figsize=(10, 7))

bars = ax.bar(k_values, top_k_accuracies, 
              color=BLUE_PALETTE['primary'], alpha=0.8, edgecolor=BLUE_PALETTE['accent'], linewidth=2)

# Add value labels on bars
for i, (k, acc) in enumerate(zip(k_values, top_k_accuracies)):
    ax.text(k, acc + 1, f'{acc:.1f}%', ha='center', va='bottom', 
            fontsize=11, fontweight='bold')

ax.set_xlabel('K (Top-K Predictions)', fontsize=13, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
ax.set_title('Top-K Accuracy Analysis', fontsize=15, fontweight='bold')
ax.set_xticks(k_values)
ax.set_ylim([0, 105])
ax.grid(True, alpha=0.3, axis='y')

# Add interpretation text
textstr = 'Top-K: Model is correct if true class\nis in top K predictions'
props = dict(boxstyle='round', facecolor=BLUE_PALETTE['light'], alpha=0.3)
ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '4_topk_accuracy.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# VISUALIZATION 5: Error Analysis Matrix (Confusion Pairs)
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 5: Error Analysis Matrix")
print("=" * 80)

# Compute confusion matrix
cm = confusion_matrix(y_true_filtered, y_pred_filtered)

# Create error matrix (only off-diagonal elements)
error_matrix = cm.copy()
np.fill_diagonal(error_matrix, 0)

# Find top confusion pairs
confusion_pairs = []
for i in range(num_classes):
    for j in range(num_classes):
        if i != j and error_matrix[i, j] > 0:
            confusion_pairs.append({
                'true': class_names[i],
                'pred': class_names[j],
                'count': error_matrix[i, j],
                'rate': error_matrix[i, j] / cm[i].sum() * 100
            })

# Sort by count
confusion_pairs.sort(key=lambda x: x['count'], reverse=True)

# Display top 10 confusion pairs
print("\n📊 Top 10 Most Common Misclassifications:")
for idx, pair in enumerate(confusion_pairs[:10], 1):
    print(f"   {idx}. {pair['true']} → {pair['pred']}: {pair['count']} samples ({pair['rate']:.1f}%)")

# Plot error matrix heatmap
fig, ax = plt.subplots(figsize=(14, 12))

# Use blue colormap
sns.heatmap(error_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names,
            cbar_kws={'label': 'Number of Misclassifications'}, ax=ax,
            linewidths=0.5, linecolor='white')

ax.set_xlabel('Predicted Label', fontsize=13, fontweight='bold')
ax.set_ylabel('True Label', fontsize=13, fontweight='bold')
ax.set_title('Error Analysis Matrix (Misclassifications Only)', fontsize=15, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '5_error_analysis_matrix.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# VISUALIZATION 6: Confidence vs Correctness Analysis
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 6: Confidence vs Correctness")
print("=" * 80)

# Create bins for confidence levels
confidence_bins = np.arange(0, 1.1, 0.1)
bin_centers = (confidence_bins[:-1] + confidence_bins[1:]) / 2

# Calculate accuracy per confidence bin
accuracies_per_bin = []
counts_per_bin = []

for i in range(len(confidence_bins) - 1):
    mask = (y_pred_max_probs >= confidence_bins[i]) & (y_pred_max_probs < confidence_bins[i+1])
    if mask.sum() > 0:
        acc = (y_true_filtered[mask] == y_pred_filtered[mask]).mean() * 100
        accuracies_per_bin.append(acc)
        counts_per_bin.append(mask.sum())
    else:
        accuracies_per_bin.append(0)
        counts_per_bin.append(0)

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Plot 1: Accuracy vs Confidence
ax1.plot(bin_centers * 100, accuracies_per_bin, marker='o', linewidth=3, markersize=10,
         color=BLUE_PALETTE['primary'], label='Accuracy per Confidence Bin')
ax1.axhline(y=np.mean(accuracies_per_bin), color=BLUE_PALETTE['accent'], 
            linestyle='--', linewidth=2, label=f'Mean Accuracy: {np.mean(accuracies_per_bin):.1f}%')
ax1.set_xlabel('Confidence Bin (%)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax1.set_title('Accuracy vs Prediction Confidence', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.set_ylim([0, 105])

# Plot 2: Sample distribution
ax2.bar(bin_centers * 100, counts_per_bin, width=8, 
        color=BLUE_PALETTE['secondary'], alpha=0.7, edgecolor=BLUE_PALETTE['accent'])
ax2.set_xlabel('Confidence Bin (%)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Samples', fontsize=12, fontweight='bold')
ax2.set_title('Sample Distribution by Confidence', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '6_confidence_vs_correctness.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# SUMMARY REPORT
# ================================================================================
print("\n" + "=" * 80)
print("SUMMARY REPORT")
print("=" * 80)

summary_path = os.path.join(OUTPUT_DIR, 'summary_report.txt')
with open(summary_path, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("ENHANCED VISUALIZATION SUMMARY REPORT\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Model: {MODEL_PATH}\n")
    f.write(f"Classes Analyzed: {num_classes} (excluding Unidentified)\n")
    f.write(f"Total Samples: {len(y_true_filtered)}\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("ROC-AUC SCORES\n")
    f.write("=" * 80 + "\n")
    f.write(f"Micro-average AUC: {roc_auc['micro']:.4f}\n\n")
    for i, class_name in enumerate(class_names):
        f.write(f"  {class_name}: {roc_auc[i]:.4f}\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("AVERAGE PRECISION SCORES\n")
    f.write("=" * 80 + "\n")
    f.write(f"Micro-average AP: {avg_precision['micro']:.4f}\n\n")
    for i, class_name in enumerate(class_names):
        f.write(f"  {class_name}: {avg_precision[i]:.4f}\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("TOP-K ACCURACY\n")
    f.write("=" * 80 + "\n")
    for k, acc in zip(k_values, top_k_accuracies):
        f.write(f"  Top-{k}: {acc:.2f}%\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("CALIBRATION\n")
    f.write("=" * 80 + "\n")
    f.write(f"  Brier Score: {brier_score:.4f}\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("TOP 10 CONFUSION PAIRS\n")
    f.write("=" * 80 + "\n")
    for idx, pair in enumerate(confusion_pairs[:10], 1):
        f.write(f"  {idx}. {pair['true']} → {pair['pred']}: {pair['count']} ({pair['rate']:.1f}%)\n")

print(f"\n✓ Summary report saved: {summary_path}")
print(f"\n📁 All visualizations saved to: {OUTPUT_DIR}")
print("\n✅ Enhanced evaluation complete!")
print("=" * 80)
