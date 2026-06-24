#!/usr/bin/env python3
"""
Generate visualizations for model performance metrics
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving files

def load_model_and_data():
    """Load the trained model and validation data"""
    print("🔍 Loading model and data...")
    
    # Load model
    model_path = "../backend/trained_model_fito.h5"
    model = tf.keras.models.load_model(model_path)
    
    # Load validation data
    val_path = r"C:\Users\HYUDADDY\Desktop\DATASET\tomato leaf diseases dataset(augmented)\validation"
    
    if not os.path.exists(val_path):
        raise FileNotFoundError(f"Validation data not found at: {val_path}")
    
    # Create data generator
    val_datagen = ImageDataGenerator(rescale=1./255)
    val_generator = val_datagen.flow_from_directory(
        val_path,
        target_size=(128, 128),
        batch_size=32,
        class_mode='categorical',
        shuffle=False
    )
    
    return model, val_generator

def plot_confusion_matrix(y_true, y_pred, class_names, output_dir='visualizations'):
    """Generate and save confusion matrix plot"""
    os.makedirs(output_dir, exist_ok=True)
    
    cm = confusion_matrix(y_true, y_pred)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    
    plt.title('Normalized Confusion Matrix', fontsize=14)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Confusion matrix saved to: {output_path}")

def plot_classification_metrics(y_true, y_pred, class_names, output_dir='visualizations'):
    """Generate and save classification metrics bar plots"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Get classification report as dictionary
    report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
    
    # Convert to DataFrame for easier plotting
    df_metrics = pd.DataFrame(report).transpose().iloc[:-3, :3]  # Remove averages
    
    # Plot metrics
    plt.figure(figsize=(14, 6))
    df_metrics[['precision', 'recall', 'f1-score']].plot(kind='bar', 
                                                       figsize=(14, 6),
                                                       color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    
    plt.title('Classification Metrics by Class', fontsize=14)
    plt.xlabel('Class', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(loc='lower right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'classification_metrics.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Classification metrics plot saved to: {output_path}")

def plot_accuracy_comparison(output_dir='visualizations'):
    """Generate accuracy comparison with banana disease model"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Data for comparison
    models = ['Tomato Model', 'Banana Model']
    metrics = {
        'Overall Accuracy': [0.87, 0.72],
        'Average F1-Score': [0.87, 0.76],
        'Best Class F1': [0.94, 0.84],
        'Worst Class F1': [0.82, 0.67]
    }
    
    df = pd.DataFrame(metrics, index=models)
    
    # Plot
    ax = df.plot(kind='bar', figsize=(12, 6), rot=0, 
                color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    plt.title('Performance Comparison: Tomato vs Banana Disease Models', fontsize=14)
    plt.ylabel('Score', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_dir, 'model_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Model comparison plot saved to: {output_path}")

def main():
    """Main function to generate all visualizations"""
    try:
        # Load model and data
        model, val_generator = load_model_and_data()
        
        # Get predictions
        print("\n🧪 Running predictions on validation set...")
        predictions = model.predict(val_generator, verbose=1)
        y_pred = np.argmax(predictions, axis=1)
        y_true = val_generator.classes
        class_names = list(val_generator.class_indices.keys())
        
        # Create visualizations
        print("\n📊 Generating visualizations...")
        plot_confusion_matrix(y_true, y_pred, class_names)
        plot_classification_metrics(y_true, y_pred, class_names)
        plot_accuracy_comparison()
        
        print("\n✅ All visualizations generated successfully!")
        print(f"📁 Check the 'visualizations' directory for output files.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
