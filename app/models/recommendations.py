"""
Pydantic models for skincare recommendations
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from .skin_analysis import SkinConditionType, SeverityLevel

class ProductCategory(str, Enum):
    """Skincare product categories"""
    CLEANSER = "cleanser"
    TONER = "toner"
    SERUM = "serum"
    MOISTURIZER = "moisturizer"
    SUNSCREEN = "sunscreen"
    TREATMENT = "treatment"
    EXFOLIANT = "exfoliant"
    MASK = "mask"
    EYE_CREAM = "eye_cream"

class IngredientType(str, Enum):
    """Active ingredient types"""
    # Anti-aging
    RETINOL = "retinol"
    VITAMIN_C = "vitamin_c"
    PEPTIDES = "peptides"
    
    # Acne treatment
    SALICYLIC_ACID = "salicylic_acid"
    BENZOYL_PEROXIDE = "benzoyl_peroxide"
    NIACINAMIDE = "niacinamide"
    
    # Hydration
    HYALURONIC_ACID = "hyaluronic_acid"
    GLYCERIN = "glycerin"
    CERAMIDES = "ceramides"
    
    # Brightening
    ALPHA_ARBUTIN = "alpha_arbutin"
    KOJIC_ACID = "kojic_acid"
    AZELAIC_ACID = "azelaic_acid"
    
    # Exfoliation
    AHA = "aha"
    BHA = "bha"
    LACTIC_ACID = "lactic_acid"

class TimeOfDay(str, Enum):
    """When to use the product"""
    MORNING = "morning"
    EVENING = "evening"
    BOTH = "both"

class RecommendedProduct(BaseModel):
    """Individual product recommendation"""
    product_id: str = Field(..., description="Unique product identifier")
    name: str
    category: ProductCategory
    brand: Optional[str] = Field(default=None)
    
    # Key ingredients
    key_ingredients: List[IngredientType] = Field(default_factory=list)
    
    # Usage instructions
    usage_frequency: str = Field(..., description="How often to use (e.g., '2-3 times per week')")
    time_of_day: TimeOfDay
    application_order: int = Field(..., ge=1, description="Order in skincare routine (1-10)")
    
    # Why recommended
    target_conditions: List[SkinConditionType] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
    
    # Product details
    price_range: Optional[str] = Field(default=None, description="Price range (e.g., '$10-20')")
    description: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    
    # Confidence and personalization
    recommendation_confidence: float = Field(..., ge=0.0, le=1.0)
    personalization_score: float = Field(..., ge=0.0, le=1.0)

class SkincareRoutine(BaseModel):
    """Complete skincare routine recommendation"""
    routine_id: str
    morning_routine: List[RecommendedProduct] = Field(default_factory=list)
    evening_routine: List[RecommendedProduct] = Field(default_factory=list)
    weekly_treatments: List[RecommendedProduct] = Field(default_factory=list)
    
    # Routine metadata
    difficulty_level: str = Field(..., description="beginner, intermediate, advanced")
    estimated_cost: Optional[str] = Field(default=None, description="Estimated monthly cost")
    time_commitment: str = Field(..., description="Daily time required (e.g., '5-10 minutes')")

class GeneralAdvice(BaseModel):
    """General skincare advice"""
    lifestyle_tips: List[str] = Field(default_factory=list)
    dietary_suggestions: List[str] = Field(default_factory=list)
    habits_to_avoid: List[str] = Field(default_factory=list)
    when_to_see_dermatologist: Optional[str] = Field(default=None)

class RecommendationResponse(BaseModel):
    """Complete recommendation response"""
    recommendation_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Analysis reference
    analysis_id: str = Field(..., description="Reference to the skin analysis")
    
    # Recommendations
    skincare_routine: SkincareRoutine
    general_advice: GeneralAdvice
    
    # Priority conditions to address
    priority_conditions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Conditions prioritized for treatment"
    )
    
    # Progress tracking
    expected_improvement_timeline: Optional[str] = Field(
        default=None,
        description="When to expect visible improvements"
    )
    follow_up_recommended: Optional[str] = Field(
        default=None,
        description="When to reassess skin condition"
    )
    
    # Metadata
    personalized: bool = Field(default=False, description="Whether recommendations are personalized")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall recommendation confidence")

class RecommendationRequest(BaseModel):
    """Request for skincare recommendations"""
    analysis_id: str = Field(..., description="ID of the skin analysis to base recommendations on")
    user_profile: Optional[Dict[str, Any]] = Field(default=None, description="User profile for personalization")
    budget_preference: Optional[str] = Field(default=None, description="budget preference: low, medium, high")
    routine_complexity: Optional[str] = Field(default="beginner", description="beginner, intermediate, advanced")
    focus_areas: Optional[List[SkinConditionType]] = Field(
        default=None,
        description="Specific conditions to focus treatment on"
    )