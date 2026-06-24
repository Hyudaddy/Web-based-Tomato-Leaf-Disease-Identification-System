#!/usr/bin/env python3
"""
Simple model evaluation without matplotlib
"""
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

def evaluate_model():
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
    print("-" * 50)
    
    for i, class_name in enumerate(class_names):
        class_mask = true_classes == i
        if np.sum(class_mask) > 0:
            class_accuracy = np.mean(predicted_classes[class_mask] == i)
            total_samples = np.sum(class_mask)
            correct_predictions = np.sum(predicted_classes[class_mask] == i)
            print(f"{class_name:40} {class_accuracy:.4f} ({correct_predictions}/{total_samples})")
    
    # Find most confused classes
    print(f"\n🚨 Common Misclassifications:")
    print("-" * 50)
    
    from collections import defaultdict
    confusion_count = defaultdict(int)
    
    for true_class, pred_class in zip(true_classes, predicted_classes):
        if true_class != pred_class:
            true_name = class_names[true_class]
            pred_name = class_names[pred_class]
            confusion_count[f"{true_name} → {pred_name}"] += 1
    
    # Sort by frequency
    sorted_confusions = sorted(confusion_count.items(), key=lambda x: x[1], reverse=True)
    
    for confusion, count in sorted_confusions[:10]:  # Top 10 misclassifications
        print(f"{confusion:50} ({count} times)")
    
    return accuracy, class_names

def suggest_improvements(accuracy):
    """Suggest improvements based on accuracy"""
    print(f"\n💡 Improvement Suggestions:")
    print("=" * 60)
    
    if accuracy < 0.7:
        print("🚨 LOW ACCURACY - Major improvements needed:")
        print("   1. Check for data quality issues")
        print("   2. Consider retraining with more data")
        print("   3. Try different model architecture")
        print("   4. Implement confidence thresholds")
    elif accuracy < 0.85:
        print("⚠️  MODERATE ACCURACY - Good but can be improved:")
        print("   1. Add more training data for weak classes")
        print("   2. Implement confidence thresholds")
        print("   3. Add data augmentation")
        print("   4. Consider ensemble methods")
    else:
        print("✅ GOOD ACCURACY - Production ready with safeguards:")
        print("   1. Implement confidence thresholds")
        print("   2. Add 'Uncertain' category for low confidence")
        print("   3. Test with real-world images")
        print("   4. Consider expert review for critical cases")
    
    print(f"\n🎯 Production Recommendations:")
    print("-" * 40)
    print("1. 📊 Confidence Thresholds:")
    print("   - High confidence (>85%): Trust the prediction")
    print("   - Medium confidence (70-85%): Show with warning")
    print("   - Low confidence (<70%): Mark as 'Uncertain'")
    print("")
    print("2. 🧪 Real-world Testing:")
    print("   - Test with images from different cameras")
    print("   - Test with different lighting conditions")
    print("   - Test with partially damaged leaves")
    print("   - Test with leaves at different growth stages")
    print("")
    print("3. 🛡️ Safety Measures:")
    print("   - Always show confidence scores to users")
    print("   - Add disclaimer about AI limitations")
    print("   - Recommend expert consultation for critical cases")
    print("   - Provide treatment suggestions, not just diagnosis")

if __name__ == "__main__":
    try:
        accuracy, class_names = evaluate_model()
        suggest_improvements(accuracy)
        
        print(f"\n🎯 Next Steps:")
        print("=" * 60)
        print("1. Review the misclassifications above")
        print("2. Test with real-world images")
        print("3. Implement confidence thresholds in your app")
        print("4. Consider retraining if accuracy is too low")
        
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        print("Make sure the validation dataset path is correct.")
