#!/usr/bin/env python3
"""
Diagnose the model class indices and order
"""
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

def diagnose_model():
    print("🔍 Diagnosing Model Class Order...")
    print("=" * 60)
    
    # Load the model
    model_path = "backend/trained_model_fito.h5"
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return
    
    try:
        model = tf.keras.models.load_model(model_path)
        print("✅ Model loaded successfully")
        
        # Get model output shape
        output_shape = model.output_shape
        print(f"📊 Model output shape: {output_shape}")
        print(f"📊 Number of classes: {output_shape[1]}")
        
        # Try to get class indices from the original training
        # This is a common issue - the class order might be different
        print("\n🔍 Checking for class indices in model metadata...")
        
        # Check if model has class_indices attribute
        if hasattr(model, 'class_indices'):
            print(f"✅ Model class_indices: {model.class_indices}")
        else:
            print("❌ No class_indices found in model")
        
        # Check model summary
        print("\n📋 Model Summary:")
        model.summary()
        
        # Test with a dummy prediction to see output format
        print("\n🧪 Testing with dummy input...")
        dummy_input = np.random.random((1, 128, 128, 3))
        prediction = model.predict(dummy_input, verbose=0)
        print(f"📊 Prediction shape: {prediction.shape}")
        print(f"📊 Sample prediction: {prediction[0]}")
        print(f"📊 Argmax index: {np.argmax(prediction[0])}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")

def check_training_data():
    """Check the original training data structure"""
    print("\n🔍 Checking Training Data Structure...")
    print("=" * 60)
    
    # Try to find the original dataset
    dataset_path = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\training"
    
    if os.path.exists(dataset_path):
        print(f"✅ Found dataset at: {dataset_path}")
        
        # List the directories (these are the class names)
        class_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
        class_dirs.sort()  # Sort alphabetically
        
        print(f"📁 Found {len(class_dirs)} classes:")
        for i, class_name in enumerate(class_dirs):
            print(f"   {i}: {class_name}")
        
        # Create a data generator to get the actual class indices
        datagen = ImageDataGenerator(rescale=1./255)
        generator = datagen.flow_from_directory(
            dataset_path,
            target_size=(128, 128),
            batch_size=1,
            class_mode='categorical',
            shuffle=False
        )
        
        print(f"\n📊 Actual class indices from training data:")
        print(f"   {generator.class_indices}")
        
        # Map indices to class names
        index_to_class = {v: k for k, v in generator.class_indices.items()}
        print(f"\n📊 Index to class mapping:")
        for i in range(len(index_to_class)):
            print(f"   {i}: {index_to_class[i]}")
            
        return index_to_class
    else:
        print(f"❌ Dataset not found at: {dataset_path}")
        return None

if __name__ == "__main__":
    diagnose_model()
    class_mapping = check_training_data()
    
    if class_mapping:
        print("\n🎯 SOLUTION:")
        print("=" * 60)
        print("Update the class_names in backend/model_handler.py to match this order:")
        print()
        for i in range(len(class_mapping)):
            print(f"            '{class_mapping[i]}',")
