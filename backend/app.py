from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import uuid
import io
from datetime import datetime
from model_handler import TomatoDiseasePredictor
from supabase_client import get_supabase_client
from admin_routes import router as admin_router

# Initialize FastAPI app
app = FastAPI(
    title="Fito - Tomato Leaf Disease Detection API",
    description="AI-powered tomato leaf disease detection using deep learning",
    version="1.0.0"
)

# Include admin routes
app.include_router(admin_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model predictor
# Get absolute path to model file (relative to this script)
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trained_model_fito_outdoor.h5")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

predictor = TomatoDiseasePredictor(model_path)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Fito - Tomato Leaf Disease Detection API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": predictor.model is not None
    }

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    """
    Predict tomato leaf disease from uploaded image
    
    Args:
        file: Image file (JPEG, PNG, etc.)
    
    Returns:
        JSON with prediction results
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="File must be an image"
            )
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Make prediction
        result = predictor.predict(image_bytes)
        
        # Check if image is unidentified
        if result.get('is_unidentified', False):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Image not recognized",
                    "prediction": "Unidentified",
                    "confidence": result['confidence'],
                    "message": "This image does not appear to be a tomato leaf or the disease is not clearly identifiable.",
                    "recommendations": result['safety_recommendations']['next_steps'],
                    "filename": file.filename
                }
            )
        
        # Save to Supabase (only for healthy and diseased predictions)
        try:
            supabase = get_supabase_client()
            
            # Generate unique filename
            file_id = str(uuid.uuid4())
            file_ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
            storage_path = f"{result['predicted_class']}/{file_id}.{file_ext}"
            
            # Upload to Supabase Storage
            supabase.storage.from_("tomato-leaves").upload(
                storage_path,
                image_bytes,
                file_options={"content-type": file.content_type}
            )
            
            # Get public URL
            image_url = supabase.storage.from_("tomato-leaves").get_public_url(storage_path)
            
            # Insert record into database
            prediction_data = {
                "id": file_id,
                "storage_path": storage_path,
                "image_url": image_url,
                "predicted_label": result['predicted_class'],
                "confidence": float(result['confidence']),
                "uploader_name": "anonymous",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            supabase.table("predictions").insert(prediction_data).execute()
            
            print(f"[SUCCESS] Saved prediction to Supabase: {file_id} - {result['predicted_class']}")
        except Exception as db_error:
            print(f"[WARNING] Failed to save to Supabase: {db_error}")
            # Continue even if database save fails
        
        return JSONResponse(content={
            "success": True,
            "prediction": result['predicted_class'],
            "confidence": result['confidence'],
            "all_predictions": result['all_predictions'],
            "filename": file.filename
        })
        
    except Exception as e:
        print(f"[ERROR] Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@app.get("/classes")
async def get_classes():
    """Get list of all disease classes"""
    return {
        "classes": predictor.class_names,
        "total_classes": len(predictor.class_names)
    }

if __name__ == "__main__":
    print("[FITO] Starting Fito API Server...")
    print("=" * 50)
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    print("=" * 50)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
