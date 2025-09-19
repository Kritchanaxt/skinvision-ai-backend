"""
Pydantic models for skin analysis requests and responses
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SkinConditionType(str, Enum):
    """Enumeration of skin condition types"""
    ACNE = "acne"
    WRINKLES = "wrinkles"
    DARK_SPOTS = "dark_spots"
    OILINESS = "oiliness"
    DRYNESS = "dryness"
    PORES = "pores"
    PIGMENTATION = "pigmentation"

class SeverityLevel(str, Enum):
    """Severity levels for skin conditions"""
    NONE = "none"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"

class SkinZone(str, Enum):
    """Face zones for analysis"""
    FOREHEAD = "forehead"
    CHEEKS = "cheeks"
    NOSE = "nose"
    CHIN = "chin"
    T_ZONE = "t_zone"
    OVERALL = "overall"

class DetectedCondition(BaseModel):
    """Individual skin condition detection result"""
    condition_type: SkinConditionType
    severity: SeverityLevel
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    affected_zones: List[SkinZone] = Field(default_factory=list)
    bounding_boxes: Optional[List[Dict[str, float]]] = Field(
        default=None, 
        description="Bounding boxes for detected issues [x, y, width, height]"
    )

class FaceDetectionResult(BaseModel):
    """Face detection result"""
    face_detected: bool
    face_count: int = 0
    face_bbox: Optional[Dict[str, float]] = Field(
        default=None,
        description="Face bounding box coordinates"
    )
    landmarks: Optional[List[Dict[str, float]]] = Field(
        default=None,
        description="Facial landmarks coordinates"
    )

class SkinAnalysisResult(BaseModel):
    """Complete skin analysis result"""
    analysis_id: str = Field(..., description="Unique analysis ID")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Face detection
    face_detection: FaceDetectionResult
    
    # Skin conditions
    detected_conditions: List[DetectedCondition] = Field(default_factory=list)
    
    # Overall skin health score
    skin_health_score: float = Field(..., ge=0.0, le=100.0, description="Overall skin health score (0-100)")
    
    # Analysis metadata
    processing_time: float = Field(..., description="Processing time in seconds")
    image_quality: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Image quality metrics"
    )

class AnalysisRequest(BaseModel):
    """Request model for skin analysis"""
    user_id: Optional[str] = Field(default=None, description="Optional user ID for personalization")
    analyze_zones: List[SkinZone] = Field(
        default=[SkinZone.OVERALL], 
        description="Specific face zones to analyze"
    )
    detailed_analysis: bool = Field(
        default=True, 
        description="Whether to include detailed condition analysis"
    )

class ImageUploadResponse(BaseModel):
    """Response for image upload"""
    upload_id: str
    filename: str
    file_size: int
    image_url: str
    timestamp: datetime = Field(default_factory=datetime.now)

class UserProfile(BaseModel):
    """User profile for personalized recommendations"""
    user_id: str
    age: Optional[int] = Field(default=None, ge=13, le=100)
    skin_type: Optional[str] = Field(default=None, description="dry, oily, combination, sensitive, normal")
    gender: Optional[str] = Field(default=None)
    current_skincare_routine: Optional[List[str]] = Field(default_factory=list)
    skin_concerns: Optional[List[str]] = Field(default_factory=list)
    allergies: Optional[List[str]] = Field(default_factory=list)
    
    @validator('skin_type')
    def validate_skin_type(cls, v):
        if v and v.lower() not in ['dry', 'oily', 'combination', 'sensitive', 'normal']:
            raise ValueError('Invalid skin type')
        return v.lower() if v else v