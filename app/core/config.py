"""
Core configuration settings for SkinVision AI Backend
"""
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Optional, Union
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # App configuration
    APP_NAME: str = "SkinVision AI Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = ["*"]
    
    @field_validator('ALLOWED_HOSTS', mode='before')
    @classmethod
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(',')]
        return v
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    UPLOAD_DIRECTORY: str = "uploads"
    
    # AI Model settings
    MODEL_CONFIDENCE_THRESHOLD: float = 0.7
    FACE_DETECTION_CONFIDENCE: float = 0.5
    
    # Skin condition mapping
    SKIN_CONDITIONS: List[str] = [
        "acne",
        "wrinkles", 
        "dark_spots",
        "oiliness",
        "dryness",
        "pores",
        "pigmentation"
    ]
    
    # Database (for future use)
    DATABASE_URL: Optional[str] = None
    
    # External API keys (for future integrations)
    OPENAI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()