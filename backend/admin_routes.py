from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from typing import Optional, List
import io
import csv
from datetime import datetime
from supabase_client import get_supabase_client

router = APIRouter(prefix="/api/admin", tags=["admin"])

class RelabelRequest(BaseModel):
    label: str

@router.get("/stats")
async def get_stats():
    """Get category statistics"""
    try:
        supabase = get_supabase_client()
        
        # Fetch all predictions
        response = supabase.table("predictions").select("predicted_label, final_label").execute()
        
        # Count by category
        counts = {}
        for item in response.data:
            label = item.get("final_label") or item.get("predicted_label")
            counts[label] = counts.get(label, 0) + 1
        
        # Convert to list
        stats = [{"category": k, "count": v} for k, v in counts.items()]
        
        return {
            "success": True,
            "stats": stats,
            "total": len(response.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dataset")
async def get_dataset(
    category: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: Optional[str] = Query(None)
):
    """Get paginated dataset with filters"""
    try:
        supabase = get_supabase_client()
        
        # Build query
        query = supabase.table("predictions").select("*", count="exact")
        
        # Apply filters
        if category and category != "All Categories":
            # Filter by either final_label or predicted_label
            query = query.or_(f"final_label.eq.{category},and(final_label.is.null,predicted_label.eq.{category})")
        
        if from_date:
            query = query.gte("created_at", from_date)
        
        if to_date:
            query = query.lte("created_at", to_date)
        
        if q:
            query = query.or_(f"storage_path.ilike.%{q}%,uploader_name.ilike.%{q}%,predicted_label.ilike.%{q}%")
        
        # Order and paginate
        offset = (page - 1) * page_size
        query = query.order("created_at", desc=True).range(offset, offset + page_size - 1)
        
        response = query.execute()
        
        return {
            "success": True,
            "data": response.data,
            "total": response.count,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/dataset/{id}/label")
async def relabel_prediction(id: str, request: RelabelRequest):
    """Update the final label of a prediction"""
    try:
        supabase = get_supabase_client()
        
        response = supabase.table("predictions").update({
            "final_label": request.label,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Prediction not found")
        
        return {
            "success": True,
            "data": response.data[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/dataset/{id}")
async def delete_prediction(id: str):
    """Delete a prediction"""
    try:
        supabase = get_supabase_client()
        
        # Get the prediction first to get storage path
        prediction = supabase.table("predictions").select("storage_path").eq("id", id).execute()
        
        if not prediction.data:
            raise HTTPException(status_code=404, detail="Prediction not found")
        
        storage_path = prediction.data[0]["storage_path"]
        
        # Delete from storage
        try:
            supabase.storage.from_("tomato-leaves").remove([storage_path])
        except Exception as storage_error:
            print(f"⚠️ Failed to delete from storage: {storage_error}")
        
        # Delete from database
        supabase.table("predictions").delete().eq("id", id).execute()
        
        return {
            "success": True,
            "message": "Prediction deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dataset/{id}/download")
async def download_image(id: str):
    """Download a single image"""
    try:
        supabase = get_supabase_client()
        
        # Get prediction
        prediction = supabase.table("predictions").select("storage_path, predicted_label").eq("id", id).execute()
        
        if not prediction.data:
            raise HTTPException(status_code=404, detail="Prediction not found")
        
        storage_path = prediction.data[0]["storage_path"]
        
        # Download from storage
        file_data = supabase.storage.from_("tomato-leaves").download(storage_path)
        
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"attachment; filename={id}.jpg"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dataset/export/csv")
async def export_csv(
    category: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    q: Optional[str] = Query(None)
):
    """Export filtered dataset as CSV"""
    try:
        supabase = get_supabase_client()
        
        # Build query (same as dataset endpoint but without pagination)
        query = supabase.table("predictions").select("*")
        
        if category and category != "All Categories":
            query = query.or_(f"final_label.eq.{category},and(final_label.is.null,predicted_label.eq.{category})")
        
        if from_date:
            query = query.gte("created_at", from_date)
        
        if to_date:
            query = query.lte("created_at", to_date)
        
        if q:
            query = query.or_(f"storage_path.ilike.%{q}%,uploader_name.ilike.%{q}%,predicted_label.ilike.%{q}%")
        
        response = query.order("created_at", desc=True).execute()
        
        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["ID", "Predicted Label", "Confidence", "Final Label", "Uploader", "Created At", "Image URL"])
        
        # Write data
        for item in response.data:
            writer.writerow([
                item.get("id"),
                item.get("predicted_label"),
                item.get("confidence"),
                item.get("final_label", ""),
                item.get("uploader_name", ""),
                item.get("created_at"),
                item.get("image_url", "")
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        filename = f"dataset_{category or 'all'}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

