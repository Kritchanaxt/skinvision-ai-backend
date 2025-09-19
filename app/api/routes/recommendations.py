"""
Skincare recommendation endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import uuid
from datetime import datetime

from app.models.recommendations import (
    RecommendationResponse,
    RecommendationRequest,
    RecommendedProduct,
    SkincareRoutine,
    ProductCategory
)
from app.models.skin_analysis import SkinConditionType, UserProfile
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter()

# Initialize recommendation engine
recommendation_engine = RecommendationEngine()

@router.post("/recommend", response_model=RecommendationResponse)
async def get_skincare_recommendations(request: RecommendationRequest):
    """
    Get personalized skincare recommendations based on skin analysis
    """
    try:
        # Generate recommendations
        recommendations = await recommendation_engine.generate_recommendations(
            analysis_id=request.analysis_id,
            user_profile=request.user_profile,
            budget_preference=request.budget_preference,
            routine_complexity=request.routine_complexity,
            focus_areas=request.focus_areas
        )
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")

@router.get("/recommend/{analysis_id}")
async def get_recommendations_by_analysis(
    analysis_id: str,
    budget: Optional[str] = None,
    complexity: str = "beginner"
):
    """
    Get recommendations for a specific analysis ID with optional parameters
    """
    request = RecommendationRequest(
        analysis_id=analysis_id,
        budget_preference=budget,
        routine_complexity=complexity
    )
    
    return await get_skincare_recommendations(request)

@router.get("/products/categories")
async def get_product_categories():
    """
    Get all available product categories
    """
    return {
        "categories": [category.value for category in ProductCategory],
        "description": "Available skincare product categories"
    }

@router.get("/products/ingredients")
async def get_active_ingredients():
    """
    Get information about active ingredients
    """
    from app.models.recommendations import IngredientType
    
    ingredient_info = {
        # Anti-aging
        IngredientType.RETINOL: {
            "name": "Retinol",
            "benefits": ["Reduces fine lines", "Improves skin texture", "Boosts collagen production"],
            "best_for": ["wrinkles", "uneven texture"],
            "usage": "evening only",
            "precautions": ["Start slowly", "Use sunscreen", "May cause initial irritation"]
        },
        IngredientType.VITAMIN_C: {
            "name": "Vitamin C",
            "benefits": ["Brightens skin", "Antioxidant protection", "Boosts collagen"],
            "best_for": ["dark spots", "dull skin", "prevention"],
            "usage": "morning preferred",
            "precautions": ["Use sunscreen", "Store properly"]
        },
        
        # Acne treatment
        IngredientType.SALICYLIC_ACID: {
            "name": "Salicylic Acid (BHA)",
            "benefits": ["Unclogs pores", "Reduces inflammation", "Exfoliates"],
            "best_for": ["acne", "blackheads", "oily skin"],
            "usage": "evening",
            "precautions": ["Start slowly", "May cause dryness"]
        },
        IngredientType.NIACINAMIDE: {
            "name": "Niacinamide",
            "benefits": ["Controls oil", "Minimizes pores", "Reduces redness"],
            "best_for": ["oily skin", "large pores", "acne"],
            "usage": "morning and evening",
            "precautions": ["Generally well-tolerated"]
        },
        
        # Hydration
        IngredientType.HYALURONIC_ACID: {
            "name": "Hyaluronic Acid",
            "benefits": ["Intense hydration", "Plumps skin", "Suitable for all skin types"],
            "best_for": ["dry skin", "dehydration", "all skin types"],
            "usage": "morning and evening",
            "precautions": ["Apply to damp skin"]
        }
    }
    
    return {
        "ingredients": {k.value: v for k, v in ingredient_info.items()},
        "total_ingredients": len(ingredient_info)
    }

@router.get("/routines/templates")
async def get_routine_templates():
    """
    Get pre-defined routine templates for different skin types
    """
    templates = {
        "oily_acne_prone": {
            "name": "Oily & Acne-Prone Skin",
            "description": "For those with oily skin and frequent breakouts",
            "morning": ["gentle_cleanser", "niacinamide_serum", "light_moisturizer", "spf"],
            "evening": ["gentle_cleanser", "salicylic_acid", "moisturizer"],
            "weekly": ["clay_mask"]
        },
        "dry_sensitive": {
            "name": "Dry & Sensitive Skin",
            "description": "For those with dry, easily irritated skin",
            "morning": ["gentle_cleanser", "hyaluronic_acid", "rich_moisturizer", "spf"],
            "evening": ["gentle_cleanser", "ceramide_serum", "night_moisturizer"],
            "weekly": ["hydrating_mask"]
        },
        "aging_concerns": {
            "name": "Anti-Aging Focus",
            "description": "For those concerned with fine lines and skin firmness",
            "morning": ["gentle_cleanser", "vitamin_c_serum", "moisturizer", "spf"],
            "evening": ["gentle_cleanser", "retinol", "rich_moisturizer"],
            "weekly": ["exfoliating_treatment"]
        },
        "combination_skin": {
            "name": "Combination Skin",
            "description": "For those with oily T-zone and normal/dry cheeks",
            "morning": ["gentle_cleanser", "lightweight_serum", "gel_moisturizer", "spf"],
            "evening": ["gentle_cleanser", "targeted_treatments", "moisturizer"],
            "weekly": ["multi_masking"]
        }
    }
    
    return {
        "templates": templates,
        "total_templates": len(templates)
    }

@router.get("/advice/general")
async def get_general_skincare_advice():
    """
    Get general skincare tips and advice
    """
    return {
        "lifestyle_tips": [
            "Stay hydrated - drink at least 8 glasses of water daily",
            "Get adequate sleep (7-9 hours) for skin repair",
            "Manage stress through meditation or exercise",
            "Avoid touching your face frequently",
            "Change pillowcases regularly",
            "Exercise regularly to improve circulation"
        ],
        "dietary_suggestions": [
            "Eat foods rich in antioxidants (berries, leafy greens)",
            "Include omega-3 fatty acids (fish, nuts, seeds)",
            "Limit dairy if you have acne-prone skin",
            "Reduce sugar and processed foods",
            "Add probiotics for gut health",
            "Include vitamin C rich foods"
        ],
        "habits_to_avoid": [
            "Over-washing your face (more than twice daily)",
            "Using harsh scrubs or aggressive exfoliation",
            "Picking at blemishes or blackheads",
            "Sleeping with makeup on",
            "Using expired skincare products",
            "Skipping sunscreen, even on cloudy days"
        ],
        "when_to_see_dermatologist": [
            "Severe acne that doesn't respond to over-the-counter treatments",
            "Sudden changes in moles or new growths",
            "Persistent redness or irritation",
            "Signs of skin infection",
            "Severe allergic reactions to products",
            "Professional treatments needed (prescription retinoids, etc.)"
        ]
    }