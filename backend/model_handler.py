import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

class TomatoDiseasePredictor:
    def __init__(self, model_path):
        """Initialize the model predictor"""
        self.model = None
        self.class_names = [
            'Bacterial Spot',
            'Early Blight', 
            'Late Blight',
            'Leaf Mold',
            'Septoria Leaf Spot',
            'Spider Mites',
            'Target Spot',
            'Yellow Leaf Curl Virus',
            'Mosaic Virus',
            'Healthy'
        ]
        self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load the trained model"""
        try:
            self.model = tf.keras.models.load_model(model_path)
            print(f"✓ Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise e
    
    def preprocess_image(self, image_bytes):
        """Preprocess image for model prediction"""
        try:
            # Open image from bytes
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to 128x128 (same as training)
            image = image.resize((128, 128))
            
            # Convert to numpy array and normalize
            image_array = np.array(image) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            raise e
    
    def predict(self, image_bytes):
        """Make prediction on the image"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_bytes)
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get the predicted class and confidence
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            predicted_class = self.class_names[predicted_class_idx]
            
            # Determine confidence level and reliability
            if confidence >= 0.90:
                confidence_level = "high"
                reliability = "reliable"
            elif confidence >= 0.70:
                confidence_level = "medium"
                reliability = "moderate"
            else:
                confidence_level = "low"
                reliability = "uncertain"
            
            # Get all predictions with confidence scores
            all_predictions = []
            for i, (class_name, conf) in enumerate(zip(self.class_names, predictions[0])):
                all_predictions.append({
                    'class': class_name,
                    'confidence': float(conf)
                })
            
            # Sort by confidence
            all_predictions.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Add safety recommendations
            safety_recommendations = self._get_safety_recommendations(predicted_class, confidence_level)
            
            return {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'confidence_level': confidence_level,
                'reliability': reliability,
                'all_predictions': all_predictions,
                'safety_recommendations': safety_recommendations
            }
            
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
            raise e
    
    def _get_safety_recommendations(self, predicted_class, confidence_level):
        """Get safety recommendations based on prediction"""
        recommendations = {
            "disclaimer": "This AI diagnosis is for guidance only. Always consult with agricultural experts for critical decisions.",
            "confidence_threshold": confidence_level,
            "next_steps": []
        }
        
        if confidence_level == "low":
            recommendations["next_steps"] = [
                "⚠️ Low confidence prediction - results may be unreliable",
                "📸 Try taking another photo with better lighting",
                "👨‍🌾 Consult with a local agricultural expert",
                "🔍 Check for multiple disease symptoms"
            ]
        elif confidence_level == "medium":
            recommendations["next_steps"] = [
                "✅ Moderate confidence - prediction is likely correct",
                "📋 Review the detailed analysis below",
                "🌱 Consider the recommended treatment",
                "👨‍🌾 Get expert confirmation for critical cases"
            ]
        else:  # high confidence
            recommendations["next_steps"] = [
                "✅ High confidence prediction - result is reliable",
                "📋 Follow the recommended treatment plan",
                "📊 Monitor plant progress after treatment",
                "🔄 Re-test if symptoms persist"
            ]
        
        # Add disease-specific recommendations
        disease_info = {
            "Bacterial Spot": {
                "treatment": "Apply copper-based fungicides",
                "prevention": "Improve air circulation, avoid overhead watering"
            },
            "Early Blight": {
                "treatment": "Remove infected leaves, apply fungicide",
                "prevention": "Crop rotation, proper spacing"
            },
            "Late Blight": {
                "treatment": "Apply systemic fungicides immediately",
                "prevention": "Avoid overhead watering, improve drainage"
            },
            "Leaf Mold": {
                "treatment": "Improve ventilation, apply fungicide",
                "prevention": "Reduce humidity, proper spacing"
            },
            "Septoria Leaf Spot": {
                "treatment": "Remove infected leaves, apply fungicide",
                "prevention": "Avoid overhead watering, crop rotation"
            },
            "Spider Mites": {
                "treatment": "Apply miticide, increase humidity",
                "prevention": "Regular monitoring, beneficial insects"
            },
            "Target Spot": {
                "treatment": "Apply fungicide, remove infected leaves",
                "prevention": "Proper spacing, good air circulation"
            },
            "Yellow Leaf Curl Virus": {
                "treatment": "Remove infected plants, control whiteflies",
                "prevention": "Use resistant varieties, control vectors"
            },
            "Mosaic Virus": {
                "treatment": "Remove infected plants immediately",
                "prevention": "Use virus-free seeds, control aphids"
            },
            "Healthy": {
                "treatment": "Continue current care practices",
                "prevention": "Maintain good growing conditions"
            }
        }
        
        if predicted_class in disease_info:
            recommendations["disease_info"] = disease_info[predicted_class]
        
        return recommendations
