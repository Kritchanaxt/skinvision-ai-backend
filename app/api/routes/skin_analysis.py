"""
Skin analysis endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
import uuid
import os
import time
from datetime import datetime
from typing import Optional

from app.models.skin_analysis import (
    SkinAnalysisResult, 
    AnalysisRequest, 
    ImageUploadResponse,
    UserProfile
)
from app.services.image_processor import ImageProcessor
from app.services.skin_analyzer import SkinAnalyzer
from app.core.config import settings

router = APIRouter()

# Initialize services
image_processor = ImageProcessor()
skin_analyzer = SkinAnalyzer()

@router.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image for skin analysis
    """
    # Validate file type
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {settings.ALLOWED_IMAGE_TYPES}"
        )
    
    # Validate file size
    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE} bytes"
        )
    
    # Generate unique filename
    upload_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    filename = f"{upload_id}.{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIRECTORY, filename)
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    
    return ImageUploadResponse(
        upload_id=upload_id,
        filename=filename,
        file_size=len(contents),
        image_url=f"/uploads/{filename}"
    )

@router.post("/analyze", response_model=SkinAnalysisResult)
async def analyze_skin(
    upload_id: str = Form(...),
    user_id: Optional[str] = Form(None),
    analyze_zones: Optional[str] = Form("overall"),
    detailed_analysis: bool = Form(True)
):
    """
    Analyze uploaded image for skin conditions
    """
    start_time = time.time()
    analysis_id = str(uuid.uuid4())
    
    # Find uploaded file
    uploaded_files = [f for f in os.listdir(settings.UPLOAD_DIRECTORY) if f.startswith(upload_id)]
    if not uploaded_files:
        raise HTTPException(status_code=404, detail="Upload not found")
    
    file_path = os.path.join(settings.UPLOAD_DIRECTORY, uploaded_files[0])
    
    try:
        # Process image
        processed_image = await image_processor.process_image(file_path)
        
        # Detect face
        face_result = await image_processor.detect_face(processed_image)
        if not face_result.face_detected:
            raise HTTPException(status_code=400, detail="No face detected in image")
        
        # Parse analyze_zones
        zones = [zone.strip() for zone in analyze_zones.split(",")]
        
        # Analyze skin conditions
        analysis_result = await skin_analyzer.analyze_skin_conditions(
            processed_image,
            face_result,
            zones=zones,
            detailed=detailed_analysis
        )
        
        processing_time = time.time() - start_time
        
        return SkinAnalysisResult(
            analysis_id=analysis_id,
            face_detection=face_result,
            detected_conditions=analysis_result.conditions,
            skin_health_score=analysis_result.health_score,
            processing_time=processing_time,
            image_quality=analysis_result.image_quality
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/analysis/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """
    Get analysis result by ID (placeholder for database integration)
    """
    # This would typically query a database
    # For now, return a placeholder response
    return JSONResponse(
        status_code=404,
        content={"detail": "Analysis result storage not implemented yet"}
    )

@router.post("/analyze-url")
async def analyze_from_url(image_url: str, request: AnalysisRequest):
    """
    Analyze skin from image URL
    """
    # This would download image from URL and process it
    # Implementation depends on security requirements
    raise HTTPException(
        status_code=501,
        detail="URL analysis not implemented yet"
    )

@router.get("/supported-conditions")
async def get_supported_conditions():
    """
    Get list of supported skin conditions
    """
    return {
        "conditions": settings.SKIN_CONDITIONS,
        "description": "List of skin conditions that can be detected by the system"
    }