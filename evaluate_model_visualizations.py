#!/usr/bin/env python3
"""
================================================================================
COMPREHENSIVE MODEL EVALUATION VISUALIZATIONS
================================================================================
This script generates all essential visualizations for evaluating a trained
image classification model.

VISUALIZATIONS INCLUDED:
1. Training vs Validation Loss/Accuracy Curves
2. Confusion Matrix (Normalized)
3. Per-Class Precision, Recall, F1-Score
4. Sample Correct/Incorrect Predictions
5. Grad-CAM Heatmaps for Explainability
6. Class Distribution
7. Prediction Confidence Histogram

Usage:
    Run this script after training to generate all evaluation plots.
    Modify the paths below to match your setup.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, precision_recall_fscore_support
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import tensorflow as tf
from datetime import datetime

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ================================================================================
# CONFIGURATION - Update these paths to match your setup
# ================================================================================
MODEL_PATH = r"C:\Users\altai\Desktop\TLDI_system\backend\trained_model_fito_outdoor.h5"
HISTORY_PATH = r"C:\Users\altai\Desktop\TLDI_system\training_history_outdoor.json"
DATASET_PATH = r"C:\Users\altai\Desktop\DATASET\tomato leaf diseases dataset(augmented)"
VAL_PATH = os.path.join(DATASET_PATH, "validation")
TRAIN_PATH = os.path.join(DATASET_PATH, "training")
OUTPUT_DIR = r"C:\Users\altai\Desktop\TLDI_system\evaluation_results"

IMG_SIZE = 224
BATCH_SIZE = 32

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("MODEL EVALUATION - COMPREHENSIVE VISUALIZATIONS")
print("=" * 80)
print(f"\n📁 Configuration:")
print(f"   • Model: {MODEL_PATH}")
print(f"   • History: {HISTORY_PATH}")
print(f"   • Validation Data: {VAL_PATH}")
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

# Load training history
with open(HISTORY_PATH, 'r') as f:
    history = json.load(f)
print(f"✓ Training history loaded: {len(history['accuracy'])} epochs")

# Load validation data
val_datagen = ImageDataGenerator(rescale=1./255)
val_generator = val_datagen.flow_from_directory(
    VAL_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False  # Important: don't shuffle for evaluation
)

# Get class names
class_names = list(val_generator.class_indices.keys())
num_classes = len(class_names)
print(f"✓ Validation data loaded: {val_generator.samples} samples, {num_classes} classes")

# ================================================================================
# VISUALIZATION 1: Training vs Validation Loss and Accuracy Curves
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 1: Training vs Validation Curves")
print("=" * 80)
print("📊 WHY THIS MATTERS:")
print("   • Shows if model is learning (loss decreasing, accuracy increasing)")
print("   • Detects overfitting (training acc >> validation acc)")
print("   • Identifies when to stop training (validation plateaus)")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Loss curves
epochs_range = range(1, len(history['loss']) + 1)
ax1.plot(epochs_range, history['loss'], 'b-', label='Training Loss', linewidth=2)
ax1.plot(epochs_range, history['val_loss'], 'r-', label='Validation Loss', linewidth=2)
ax1.set_xlabel('Epoch', fontsize=12, fontweight='bold')
ax1.set_ylabel('Loss', fontsize=12, fontweight='bold')
ax1.set_title('Training vs Validation Loss', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Add annotations for best epoch
best_epoch = np.argmin(history['val_loss']) + 1
ax1.axvline(x=best_epoch, color='g', linestyle='--', alpha=0.7, label=f'Best Epoch: {best_epoch}')
ax1.legend(fontsize=11)

# Plot 2: Accuracy curves
ax2.plot(epochs_range, history['accuracy'], 'b-', label='Training Accuracy', linewidth=2)
ax2.plot(epochs_range, history['val_accuracy'], 'r-', label='Validation Accuracy', linewidth=2)
ax2.set_xlabel('Epoch', fontsize=12, fontweight='bold')
ax2.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
ax2.set_title('Training vs Validation Accuracy', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.axvline(x=best_epoch, color='g', linestyle='--', alpha=0.7, label=f'Best Epoch: {best_epoch}')
ax2.legend(fontsize=11)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '1_training_curves.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# VISUALIZATION 2: Confusion Matrix (Normalized)
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 2: Confusion Matrix")
print("=" * 80)
print("📊 WHY THIS MATTERS:")
print("   • Shows which classes are confused with each other")
print("   • Identifies systematic misclassifications")
print("   • Helps understand model weaknesses")

# Get predictions
print("   Generating predictions on validation set...")
y_true = val_generator.classes
y_pred_probs = model.predict(val_generator, verbose=1)
y_pred = np.argmax(y_pred_probs, axis=1)

# Compute confusion matrix
cm = confusion_matrix(y_true, y_pred)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

# Plot confusion matrix
fig, ax = plt.subplots(figsize=(14, 12))
sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names,
            cbar_kws={'label': 'Normalized Frequency'}, ax=ax)
ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
ax.set_title('Confusion Matrix (Normalized)', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

output_path = os.path.join(OUTPUT_DIR, '2_confusion_matrix.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# VISUALIZATION 3: Per-Class Precision, Recall, F1-Score
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 3: Per-Class Metrics")
print("=" * 80)
print("📊 WHY THIS MATTERS:")
print("   • Precision: How many predicted positives are actually positive")
print("   • Recall: How many actual positives were correctly identified")
print("   • F1-Score: Harmonic mean of precision and recall (overall quality)")

# Calculate metrics
precision, recall, f1, support = precision_recall_fscore_support(
    y_true, y_pred, average=None, labels=range(num_classes)
)

# Create DataFrame for better visualization
metrics_data = {
    'Class': class_names,
    'Precision': precision,
    'Recall': recall,
    'F1-Score': f1,
    'Support': support
}

# Plot metrics
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(class_names))
width = 0.25

bars1 = ax.bar(x - width, precision, width, label='Precision', alpha=0.8)
bars2 = ax.bar(x, recall, width, label='Recall', alpha=0.8)
bars3 = ax.bar(x + width, f1, width, label='F1-Score', alpha=0.8)

ax.set_xlabel('Class', fontsize=12, fontweight='bold')
ax.set_ylabel('Score', fontsize=12, fontweight='bold')
ax.set_title('Per-Class Performance Metrics', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(class_names, rotation=45, ha='right')
ax.legend(fontsize=11)
ax.set_ylim([0, 1.1])
ax.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '3_per_class_metrics.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_path}")
plt.close()

# Save metrics to text file
metrics_text_path = os.path.join(OUTPUT_DIR, '3_classification_report.txt')
with open(metrics_text_path, 'w') as f:
    f.write("CLASSIFICATION REPORT\n")
    f.write("=" * 80 + "\n\n")
    report = classification_report(y_true, y_pred, target_names=class_names, digits=4)
    f.write(report)
print(f"✓ Saved: {metrics_text_path}")

# ================================================================================
# VISUALIZATION 4: Sample Correct and Incorrect Predictions
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 4: Sample Predictions")
print("=" * 80)
print("📊 WHY THIS MATTERS:")
print("   • Visual inspection of what the model gets right/wrong")
print("   • Helps identify patterns in errors")
print("   • Shows confidence levels for predictions")

# Find correct and incorrect predictions
correct_indices = np.where(y_true == y_pred)[0]
incorrect_indices = np.where(y_true != y_pred)[0]

# Sample 8 correct and 8 incorrect
num_samples = min(8, len(correct_indices), len(incorrect_indices))
correct_samples = np.random.choice(correct_indices, num_samples, replace=False)
incorrect_samples = np.random.choice(incorrect_indices, num_samples, replace=False)

def plot_predictions(indices, title, filename, is_correct=True):
    """Helper function to plot prediction samples"""
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    for idx, ax in enumerate(axes.flat):
        if idx >= len(indices):
            ax.axis('off')
            continue
            
        sample_idx = indices[idx]
        
        # Get image path
        file_idx = sample_idx
        current_count = 0
        img_path = None
        
        for class_name in class_names:
            class_path = os.path.join(VAL_PATH, class_name)
            class_files = sorted([f for f in os.listdir(class_path) 
                                if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            
            if current_count + len(class_files) > file_idx:
                img_file = class_files[file_idx - current_count]
                img_path = os.path.join(class_path, img_file)
                break
            current_count += len(class_files)
        
        if img_path and os.path.exists(img_path):
            img = load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
            ax.imshow(img)
            
            true_label = class_names[y_true[sample_idx]]
            pred_label = class_names[y_pred[sample_idx]]
            confidence = y_pred_probs[sample_idx][y_pred[sample_idx]] * 100
            
            if is_correct:
                title_text = f"✓ {true_label}\nConf: {confidence:.1f}%"
                title_color = 'green'
            else:
                title_text = f"✗ True: {true_label}\nPred: {pred_label}\nConf: {confidence:.1f}%"
                title_color = 'red'
            
            ax.set_title(title_text, fontsize=9, color=title_color, fontweight='bold')
        
        ax.axis('off')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

# Plot correct predictions
plot_predictions(correct_samples, 
                'Correct Predictions (High Confidence)', 
                '4a_correct_predictions.png', 
                is_correct=True)

# Plot incorrect predictions
plot_predictions(incorrect_samples, 
                'Incorrect Predictions (Misclassifications)', 
                '4b_incorrect_predictions.png', 
                is_correct=False)

# ================================================================================
# VISUALIZATION 5: Grad-CAM Heatmaps for Model Explainability
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 5: Grad-CAM Heatmaps")
print("=" * 80)
print("📊 WHY THIS MATTERS:")
print("   • Shows WHICH parts of the image the model focuses on")
print("   • Validates that model looks at relevant features (leaves, not background)")
print("   • Builds trust in model decisions")

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    """Generate Grad-CAM heatmap"""
    # Create a model that maps the input image to the activations of the last conv layer
    grad_model = Model(
        inputs=[model.inputs],
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )
    
    # Compute gradient of top predicted class for our input image
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]
    
    # Gradient of the output neuron with regard to the output feature map
    grads = tape.gradient(class_channel, last_conv_layer_output)
    
    # Mean intensity of the gradient over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Multiply each channel by "how important this channel is"
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Normalize heatmap
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

# Find last convolutional layer (usually in the base model)
last_conv_layer_name = None
for layer in reversed(model.layers):
    if 'conv' in layer.name.lower():
        last_conv_layer_name = layer.name
        break

if last_conv_layer_name is None:
    print("⚠️  No convolutional layer found, skipping Grad-CAM")
else:
    print(f"   Using layer: {last_conv_layer_name}")
    
    # Generate Grad-CAM for 8 random samples
    sample_indices = np.random.choice(len(y_true), min(8, len(y_true)), replace=False)
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle('Grad-CAM: Model Attention Heatmaps', fontsize=16, fontweight='bold')
    
    for idx, ax in enumerate(axes.flat):
        if idx >= len(sample_indices):
            ax.axis('off')
            continue
        
        sample_idx = sample_indices[idx]
        
        # Get image
        file_idx = sample_idx
        current_count = 0
        img_path = None
        
        for class_name in class_names:
            class_path = os.path.join(VAL_PATH, class_name)
            class_files = sorted([f for f in os.listdir(class_path) 
                                if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            
            if current_count + len(class_files) > file_idx:
                img_file = class_files[file_idx - current_count]
                img_path = os.path.join(class_path, img_file)
                break
            current_count += len(class_files)
        
        if img_path and os.path.exists(img_path):
            # Load and preprocess image
            img = load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0
            
            # Generate heatmap
            heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)
            
            # Rescale heatmap to image size
            heatmap = np.uint8(255 * heatmap)
            heatmap = tf.image.resize(heatmap[..., np.newaxis], (IMG_SIZE, IMG_SIZE))
            heatmap = heatmap.numpy().squeeze()
            
            # Superimpose heatmap on original image
            ax.imshow(img)
            ax.imshow(heatmap, cmap='jet', alpha=0.4)
            
            pred_label = class_names[y_pred[sample_idx]]
            confidence = y_pred_probs[sample_idx][y_pred[sample_idx]] * 100
            ax.set_title(f"{pred_label}\n{confidence:.1f}%", fontsize=9, fontweight='bold')
        
        ax.axis('off')
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, '5_gradcam_heatmaps.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

# ================================================================================
# VISUALIZATION 6: Class Distribution
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 6: Class Distribution")
print("=" * 80)
print("📊 WHY THIS MATTERS:")
print("   • Shows if dataset is balanced or imbalanced")
print("   • Explains why some classes may perform worse")
print("   • Validates that class weights are needed")

# Count samples per class in training and validation
train_counts = []
val_counts = []

for class_name in class_names:
    train_class_path = os.path.join(TRAIN_PATH, class_name)
    val_class_path = os.path.join(VAL_PATH, class_name)
    
    train_count = len([f for f in os.listdir(train_class_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    val_count = len([f for f in os.listdir(val_class_path) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    train_counts.append(train_count)
    val_counts.append(val_count)

# Plot distribution
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(class_names))
width = 0.35

bars1 = ax.bar(x - width/2, train_counts, width, label='Training', alpha=0.8)
bars2 = ax.bar(x + width/2, val_counts, width, label='Validation', alpha=0.8)

ax.set_xlabel('Class', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Samples', fontsize=12, fontweight='bold')
ax.set_title('Class Distribution in Dataset', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(class_names, rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '6_class_distribution.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# VISUALIZATION 7: Prediction Confidence Histogram
# ================================================================================
print("\n" + "=" * 80)
print("VISUALIZATION 7: Prediction Confidence Distribution")
print("=" * 80)
print("📊 WHY THIS MATTERS:")
print("   • Shows how confident the model is in its predictions")
print("   • High confidence = model is sure, Low confidence = model is uncertain")
print("   • Helps set confidence thresholds for production")

# Get max confidence for each prediction
max_confidences = np.max(y_pred_probs, axis=1) * 100

# Separate correct and incorrect predictions
correct_confidences = max_confidences[y_true == y_pred]
incorrect_confidences = max_confidences[y_true != y_pred]

# Plot histogram
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Overall confidence distribution
ax1.hist(max_confidences, bins=50, alpha=0.7, color='blue', edgecolor='black')
ax1.axvline(x=np.mean(max_confidences), color='red', linestyle='--', 
            linewidth=2, label=f'Mean: {np.mean(max_confidences):.1f}%')
ax1.axvline(x=np.median(max_confidences), color='green', linestyle='--', 
            linewidth=2, label=f'Median: {np.median(max_confidences):.1f}%')
ax1.set_xlabel('Confidence (%)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax1.set_title('Overall Prediction Confidence Distribution', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3, axis='y')

# Correct vs Incorrect confidence
ax2.hist(correct_confidences, bins=30, alpha=0.6, color='green', 
         label=f'Correct (n={len(correct_confidences)})', edgecolor='black')
ax2.hist(incorrect_confidences, bins=30, alpha=0.6, color='red', 
         label=f'Incorrect (n={len(incorrect_confidences)})', edgecolor='black')
ax2.set_xlabel('Confidence (%)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax2.set_title('Confidence: Correct vs Incorrect Predictions', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '7_confidence_histogram.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_path}")
plt.close()

# ================================================================================
# SUMMARY REPORT
# ================================================================================
print("\n" + "=" * 80)
print("EVALUATION SUMMARY")
print("=" * 80)

# Calculate overall metrics
overall_accuracy = np.mean(y_true == y_pred) * 100
avg_precision = np.mean(precision) * 100
avg_recall = np.mean(recall) * 100
avg_f1 = np.mean(f1) * 100

print(f"\n📊 Overall Performance:")
print(f"   • Accuracy: {overall_accuracy:.2f}%")
print(f"   • Average Precision: {avg_precision:.2f}%")
print(f"   • Average Recall: {avg_recall:.2f}%")
print(f"   • Average F1-Score: {avg_f1:.2f}%")

print(f"\n📈 Confidence Statistics:")
print(f"   • Mean Confidence: {np.mean(max_confidences):.2f}%")
print(f"   • Median Confidence: {np.median(max_confidences):.2f}%")
print(f"   • Correct Predictions Mean Confidence: {np.mean(correct_confidences):.2f}%")
print(f"   • Incorrect Predictions Mean Confidence: {np.mean(incorrect_confidences):.2f}%")

print(f"\n📁 All visualizations saved to: {OUTPUT_DIR}")
print("\n✅ Evaluation complete!")
print("=" * 80)
