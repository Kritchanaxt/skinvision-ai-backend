"""
SkinVision AI Backend
AI-based Facial Skin Analysis for Personalized Skincare Recommendation
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.api.routes import skin_analysis, recommendations, health
from app.core.config import settings

# Create FastAPI instance
app = FastAPI(
    title="SkinVision AI Backend",
    description="AI-based Facial Skin Analysis for Personalized Skincare Recommendation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded images
uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)
    
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(skin_analysis.router, prefix="/api/v1", tags=["Skin Analysis"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["Recommendations"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🌟 Welcome to SkinVision AI Backend",
        "description": "AI-based Facial Skin Analysis for Personalized Skincare Recommendation",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )