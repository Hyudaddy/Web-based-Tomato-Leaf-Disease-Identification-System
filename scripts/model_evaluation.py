#!/usr/bin/env python3
"""
Comprehensive model evaluation and analysis
"""
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

def evaluate_model_performance():
    """Evaluate model performance on validation data"""
    print("🔍 Evaluating Model Performance...")
    print("=" * 60)
    
    # Load model
    model_path = "backend/trained_model_fito.h5"
    model = tf.keras.models.load_model(model_path)
    
    # Load validation data
    val_path = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation"
    
    if not os.path.exists(val_path):
        print(f"❌ Validation data not found at: {val_path}")
        return
    
    # Create data generator
    val_datagen = ImageDataGenerator(rescale=1./255)
    val_generator = val_datagen.flow_from_directory(
        val_path,
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical',
        shuffle=False
    )
    
    print(f"✅ Loaded validation data: {val_generator.samples} samples")
    print(f"📊 Classes: {val_generator.class_indices}")
    
    # Get predictions
    print("\n🧪 Running predictions on validation set...")
    predictions = model.predict(val_generator, verbose=1)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = val_generator.classes
    
    # Calculate accuracy
    accuracy = np.mean(predicted_classes == true_classes)
    print(f"\n📊 Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Class-wise performance
    class_names = list(val_generator.class_indices.keys())
    print(f"\n📊 Class-wise Performance:")
    print("-" * 40)
    
    for i, class_name in enumerate(class_names):
        class_mask = true_classes == i
        if np.sum(class_mask) > 0:
            class_accuracy = np.mean(predicted_classes[class_mask] == i)
            print(f"{class_name:30} {class_accuracy:.4f} ({class_accuracy*100:.2f}%)")
    
    # Generate classification report
    print(f"\n📋 Detailed Classification Report:")
    print("=" * 60)
    report = classification_report(true_classes, predicted_classes, 
                                  target_names=class_names, 
                                  digits=4)
    print(report)
    
    return predictions, true_classes, class_names

def analyze_confusion_matrix(true_classes, predicted_classes, class_names):
    """Analyze confusion matrix to identify common misclassifications"""
    print(f"\n🔍 Confusion Matrix Analysis:")
    print("=" * 60)
    
    cm = confusion_matrix(true_classes, predicted_classes)
    
    # Find most confused classes
    print("🚨 Most Common Misclassifications:")
    print("-" * 40)
    
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            if i != j and cm[i, j] > 0:
                print(f"{class_names[i]:30} → {class_names[j]:30} ({cm[i, j]} times)")
    
    return cm

def suggest_improvements():
    """Suggest improvements for model performance"""
    print(f"\n💡 Suggestions for Model Improvement:")
    print("=" * 60)
    
    suggestions = [
        "1. 📊 Data Quality:",
        "   - Check for mislabeled images in training data",
        "   - Ensure balanced dataset across all classes",
        "   - Add more diverse images for underperforming classes",
        "",
        "2. 🔧 Model Architecture:",
        "   - Try different base models (EfficientNet, ResNet)",
        "   - Increase model complexity (more layers)",
        "   - Adjust learning rate and training epochs",
        "",
        "3. 📈 Training Improvements:",
        "   - Use more data augmentation",
        "   - Implement class weights for imbalanced data",
        "   - Use learning rate scheduling",
        "   - Add regularization techniques",
        "",
        "4. 🧪 Testing Strategy:",
        "   - Test with real-world images from different conditions",
        "   - Test with images from different cameras/lighting",
        "   - Test with partially damaged or unclear images",
        "",
        "5. 🎯 Production Considerations:",
        "   - Set confidence thresholds (e.g., only predict if confidence > 80%)",
        "   - Add 'Uncertain' category for low-confidence predictions",
        "   - Implement ensemble methods (multiple models)",
        "   - Add human expert review for critical cases"
    ]
    
    for suggestion in suggestions:
        print(suggestion)

def create_confidence_analysis():
    """Analyze prediction confidence levels"""
    print(f"\n🎯 Confidence Analysis:")
    print("=" * 60)
    
    # This would analyze the confidence scores from predictions
    print("💡 Confidence Threshold Recommendations:")
    print("   - High Confidence (>90%): Reliable predictions")
    print("   - Medium Confidence (70-90%): Good predictions, but verify")
    print("   - Low Confidence (<70%): Uncertain, recommend expert review")
    print("   - Very Low Confidence (<50%): Likely incorrect, don't trust")

if __name__ == "__main__":
    try:
        predictions, true_classes, class_names = evaluate_model_performance()
        cm = analyze_confusion_matrix(true_classes, predictions.argmax(axis=1), class_names)
        suggest_improvements()
        create_confidence_analysis()
        
        print(f"\n🎯 Key Takeaways:")
        print("=" * 60)
        print("1. Check the confusion matrix above for specific misclassifications")
        print("2. Consider retraining with more data for problematic classes")
        print("3. Implement confidence thresholds in production")
        print("4. Always test with real-world images before deployment")
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        print("Make sure the validation dataset path is correct.")
