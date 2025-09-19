"""
Rule-based skincare recommendation engine
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import json

from app.models.recommendations import (
    RecommendationResponse,
    SkincareRoutine,
    RecommendedProduct,
    GeneralAdvice,
    ProductCategory,
    IngredientType,
    TimeOfDay
)
from app.models.skin_analysis import SkinConditionType, SeverityLevel
from app.core.config import settings

class RecommendationEngine:
    """
    Rule-based recommendation engine for skincare products and routines
    """
    
    def __init__(self):
        self.product_database = self._initialize_product_database()
        self.recommendation_rules = self._initialize_recommendation_rules()
        self.routine_templates = self._initialize_routine_templates()
    
    async def generate_recommendations(
        self,
        analysis_id: str,
        user_profile: Optional[Dict[str, Any]] = None,
        budget_preference: Optional[str] = None,
        routine_complexity: str = "beginner",
        focus_areas: Optional[List[SkinConditionType]] = None
    ) -> RecommendationResponse:
        """
        Generate personalized skincare recommendations
        
        Args:
            analysis_id: ID of the skin analysis
            user_profile: User profile information
            budget_preference: Budget preference (low, medium, high)
            routine_complexity: Routine complexity level
            focus_areas: Specific conditions to focus on
            
        Returns:
            Complete recommendation response
        """
        recommendation_id = str(uuid.uuid4())
        
        # TODO: In production, fetch actual analysis results from database
        # For now, simulate analysis results
        mock_conditions = self._get_mock_analysis_conditions()
        
        # Determine priority conditions
        priority_conditions = self._determine_priority_conditions(
            mock_conditions, focus_areas
        )
        
        # Generate product recommendations
        recommended_products = self._recommend_products(
            priority_conditions,
            user_profile,
            budget_preference,
            routine_complexity
        )
        
        # Create skincare routine
        routine = self._create_skincare_routine(
            recommended_products,
            routine_complexity
        )
        
        # Generate general advice
        general_advice = self._generate_general_advice(priority_conditions, user_profile)
        
        # Calculate confidence score
        confidence_score = self._calculate_recommendation_confidence(
            priority_conditions,
            user_profile is not None,
            routine_complexity
        )
        
        return RecommendationResponse(
            recommendation_id=recommendation_id,
            analysis_id=analysis_id,
            skincare_routine=routine,
            general_advice=general_advice,
            priority_conditions=self._format_priority_conditions(priority_conditions),
            expected_improvement_timeline=self._estimate_improvement_timeline(priority_conditions),
            follow_up_recommended="4-6 weeks",
            personalized=user_profile is not None,
            confidence_score=confidence_score
        )
    
    def _initialize_product_database(self) -> Dict[str, List[RecommendedProduct]]:
        """Initialize mock product database organized by category"""
        return {
            ProductCategory.CLEANSER.value: [
                RecommendedProduct(
                    product_id="cleanser_001",
                    name="Gentle Foaming Cleanser",
                    category=ProductCategory.CLEANSER,
                    brand="SkinCare Pro",
                    key_ingredients=[IngredientType.GLYCERIN],
                    usage_frequency="twice daily",
                    time_of_day=TimeOfDay.BOTH,
                    application_order=1,
                    target_conditions=[SkinConditionType.OILINESS, SkinConditionType.ACNE],
                    benefits=["Removes excess oil", "Gentle on skin", "Maintains skin barrier"],
                    price_range="$8-15",
                    recommendation_confidence=0.9,
                    personalization_score=0.7
                ),
                RecommendedProduct(
                    product_id="cleanser_002",
                    name="Hydrating Cream Cleanser",
                    category=ProductCategory.CLEANSER,
                    brand="Gentle Care",
                    key_ingredients=[IngredientType.CERAMIDES, IngredientType.HYALURONIC_ACID],
                    usage_frequency="twice daily",
                    time_of_day=TimeOfDay.BOTH,
                    application_order=1,
                    target_conditions=[SkinConditionType.DRYNESS],
                    benefits=["Hydrates while cleansing", "Strengthens skin barrier", "Non-stripping"],
                    price_range="$12-20",
                    recommendation_confidence=0.85,
                    personalization_score=0.8
                )
            ],
            ProductCategory.SERUM.value: [
                RecommendedProduct(
                    product_id="serum_001",
                    name="Niacinamide 10% Serum",
                    category=ProductCategory.SERUM,
                    brand="Active Solutions",
                    key_ingredients=[IngredientType.NIACINAMIDE],
                    usage_frequency="once daily",
                    time_of_day=TimeOfDay.BOTH,
                    application_order=3,
                    target_conditions=[SkinConditionType.ACNE, SkinConditionType.OILINESS, SkinConditionType.PORES],
                    benefits=["Controls oil production", "Minimizes pores", "Reduces inflammation"],
                    price_range="$6-12",
                    recommendation_confidence=0.95,
                    personalization_score=0.9
                ),
                RecommendedProduct(
                    product_id="serum_002",
                    name="Vitamin C 20% Serum",
                    category=ProductCategory.SERUM,
                    brand="Bright Skin",
                    key_ingredients=[IngredientType.VITAMIN_C],
                    usage_frequency="once daily",
                    time_of_day=TimeOfDay.MORNING,
                    application_order=3,
                    target_conditions=[SkinConditionType.DARK_SPOTS, SkinConditionType.PIGMENTATION],
                    benefits=["Brightens skin", "Fades dark spots", "Antioxidant protection"],
                    price_range="$15-25",
                    recommendation_confidence=0.88,
                    personalization_score=0.85
                ),
                RecommendedProduct(
                    product_id="serum_003",
                    name="Hyaluronic Acid Serum",
                    category=ProductCategory.SERUM,
                    brand="Hydro Plus",
                    key_ingredients=[IngredientType.HYALURONIC_ACID],
                    usage_frequency="twice daily",
                    time_of_day=TimeOfDay.BOTH,
                    application_order=3,
                    target_conditions=[SkinConditionType.DRYNESS],
                    benefits=["Intense hydration", "Plumps skin", "Suitable for all skin types"],
                    price_range="$10-18",
                    recommendation_confidence=0.92,
                    personalization_score=0.88
                )
            ],
            ProductCategory.TREATMENT.value: [
                RecommendedProduct(
                    product_id="treatment_001",
                    name="Retinol 0.5% Treatment",
                    category=ProductCategory.TREATMENT,
                    brand="Anti-Age Pro",
                    key_ingredients=[IngredientType.RETINOL],
                    usage_frequency="3 times per week",
                    time_of_day=TimeOfDay.EVENING,
                    application_order=4,
                    target_conditions=[SkinConditionType.WRINKLES, SkinConditionType.ACNE],
                    benefits=["Reduces fine lines", "Improves texture", "Boosts collagen"],
                    price_range="$20-35",
                    recommendation_confidence=0.9,
                    personalization_score=0.85
                ),
                RecommendedProduct(
                    product_id="treatment_002",
                    name="Salicylic Acid 2% Treatment",
                    category=ProductCategory.TREATMENT,
                    brand="Clear Skin",
                    key_ingredients=[IngredientType.SALICYLIC_ACID],
                    usage_frequency="every other day",
                    time_of_day=TimeOfDay.EVENING,
                    application_order=4,
                    target_conditions=[SkinConditionType.ACNE, SkinConditionType.PORES],
                    benefits=["Unclogs pores", "Reduces breakouts", "Gentle exfoliation"],
                    price_range="$12-22",
                    recommendation_confidence=0.87,
                    personalization_score=0.82
                )
            ],
            ProductCategory.MOISTURIZER.value: [
                RecommendedProduct(
                    product_id="moisturizer_001",
                    name="Lightweight Gel Moisturizer",
                    category=ProductCategory.MOISTURIZER,
                    brand="Fresh Face",
                    key_ingredients=[IngredientType.HYALURONIC_ACID, IngredientType.NIACINAMIDE],
                    usage_frequency="twice daily",
                    time_of_day=TimeOfDay.BOTH,
                    application_order=5,
                    target_conditions=[SkinConditionType.OILINESS],
                    benefits=["Non-greasy hydration", "Controls oil", "Won't clog pores"],
                    price_range="$14-24",
                    recommendation_confidence=0.88,
                    personalization_score=0.8
                ),
                RecommendedProduct(
                    product_id="moisturizer_002",
                    name="Rich Repair Cream",
                    category=ProductCategory.MOISTURIZER,
                    brand="Nourish Plus",
                    key_ingredients=[IngredientType.CERAMIDES, IngredientType.PEPTIDES],
                    usage_frequency="twice daily",
                    time_of_day=TimeOfDay.BOTH,
                    application_order=5,
                    target_conditions=[SkinConditionType.DRYNESS, SkinConditionType.WRINKLES],
                    benefits=["Deep hydration", "Strengthens barrier", "Anti-aging benefits"],
                    price_range="$18-30",
                    recommendation_confidence=0.9,
                    personalization_score=0.85
                )
            ],
            ProductCategory.SUNSCREEN.value: [
                RecommendedProduct(
                    product_id="sunscreen_001",
                    name="Broad Spectrum SPF 30",
                    category=ProductCategory.SUNSCREEN,
                    brand="Sun Shield",
                    key_ingredients=[],
                    usage_frequency="daily",
                    time_of_day=TimeOfDay.MORNING,
                    application_order=6,
                    target_conditions=[],  # Preventive for all conditions
                    benefits=["UV protection", "Prevents premature aging", "Non-comedogenic"],
                    price_range="$10-18",
                    recommendation_confidence=1.0,
                    personalization_score=0.9
                )
            ]
        }
    
    def _initialize_recommendation_rules(self) -> Dict[SkinConditionType, Dict]:
        """Initialize recommendation rules for each skin condition"""
        return {
            SkinConditionType.ACNE: {
                "primary_ingredients": [IngredientType.SALICYLIC_ACID, IngredientType.NIACINAMIDE],
                "secondary_ingredients": [IngredientType.BENZOYL_PEROXIDE],
                "avoid_ingredients": [],
                "product_categories": [ProductCategory.CLEANSER, ProductCategory.SERUM, ProductCategory.TREATMENT],
                "severity_modifiers": {
                    SeverityLevel.MILD: {"frequency_multiplier": 0.8},
                    SeverityLevel.MODERATE: {"frequency_multiplier": 1.0},
                    SeverityLevel.SEVERE: {"frequency_multiplier": 1.2}
                }
            },
            SkinConditionType.WRINKLES: {
                "primary_ingredients": [IngredientType.RETINOL, IngredientType.VITAMIN_C],
                "secondary_ingredients": [IngredientType.PEPTIDES],
                "avoid_ingredients": [],
                "product_categories": [ProductCategory.SERUM, ProductCategory.TREATMENT, ProductCategory.MOISTURIZER],
                "severity_modifiers": {
                    SeverityLevel.MILD: {"frequency_multiplier": 0.8},
                    SeverityLevel.MODERATE: {"frequency_multiplier": 1.0},
                    SeverityLevel.SEVERE: {"frequency_multiplier": 1.3}
                }
            },
            SkinConditionType.DARK_SPOTS: {
                "primary_ingredients": [IngredientType.VITAMIN_C, IngredientType.ALPHA_ARBUTIN],
                "secondary_ingredients": [IngredientType.NIACINAMIDE, IngredientType.AZELAIC_ACID],
                "avoid_ingredients": [],
                "product_categories": [ProductCategory.SERUM, ProductCategory.TREATMENT],
                "severity_modifiers": {
                    SeverityLevel.MILD: {"frequency_multiplier": 0.9},
                    SeverityLevel.MODERATE: {"frequency_multiplier": 1.0},
                    SeverityLevel.SEVERE: {"frequency_multiplier": 1.2}
                }
            },
            SkinConditionType.OILINESS: {
                "primary_ingredients": [IngredientType.NIACINAMIDE, IngredientType.SALICYLIC_ACID],
                "secondary_ingredients": [IngredientType.AHA],
                "avoid_ingredients": [],
                "product_categories": [ProductCategory.CLEANSER, ProductCategory.SERUM, ProductCategory.MOISTURIZER],
                "severity_modifiers": {
                    SeverityLevel.MILD: {"frequency_multiplier": 0.8},
                    SeverityLevel.MODERATE: {"frequency_multiplier": 1.0},
                    SeverityLevel.SEVERE: {"frequency_multiplier": 1.1}
                }
            },
            SkinConditionType.DRYNESS: {
                "primary_ingredients": [IngredientType.HYALURONIC_ACID, IngredientType.CERAMIDES],
                "secondary_ingredients": [IngredientType.GLYCERIN],
                "avoid_ingredients": [IngredientType.SALICYLIC_ACID, IngredientType.AHA],
                "product_categories": [ProductCategory.CLEANSER, ProductCategory.SERUM, ProductCategory.MOISTURIZER],
                "severity_modifiers": {
                    SeverityLevel.MILD: {"frequency_multiplier": 1.0},
                    SeverityLevel.MODERATE: {"frequency_multiplier": 1.2},
                    SeverityLevel.SEVERE: {"frequency_multiplier": 1.4}
                }
            }
        }
    
    def _initialize_routine_templates(self) -> Dict[str, Dict]:
        """Initialize routine templates based on complexity"""
        return {
            "beginner": {
                "max_products": 4,
                "max_actives": 1,
                "required_categories": [ProductCategory.CLEANSER, ProductCategory.MOISTURIZER, ProductCategory.SUNSCREEN]
            },
            "intermediate": {
                "max_products": 6,
                "max_actives": 2,
                "required_categories": [ProductCategory.CLEANSER, ProductCategory.SERUM, ProductCategory.MOISTURIZER, ProductCategory.SUNSCREEN]
            },
            "advanced": {
                "max_products": 8,
                "max_actives": 3,
                "required_categories": [ProductCategory.CLEANSER, ProductCategory.SERUM, ProductCategory.TREATMENT, ProductCategory.MOISTURIZER, ProductCategory.SUNSCREEN]
            }
        }
    
    def _get_mock_analysis_conditions(self) -> List[Dict]:
        """Generate mock analysis conditions for testing"""
        return [
            {
                "condition_type": SkinConditionType.ACNE,
                "severity": SeverityLevel.MODERATE,
                "confidence": 0.85
            },
            {
                "condition_type": SkinConditionType.OILINESS,
                "severity": SeverityLevel.MILD,
                "confidence": 0.78
            },
            {
                "condition_type": SkinConditionType.PORES,
                "severity": SeverityLevel.MODERATE,
                "confidence": 0.82
            }
        ]
    
    def _determine_priority_conditions(
        self,
        conditions: List[Dict],
        focus_areas: Optional[List[SkinConditionType]]
    ) -> List[Dict]:
        """Determine which conditions to prioritize for treatment"""
        # Sort by severity and confidence
        priority_conditions = sorted(
            conditions,
            key=lambda x: (
                x["severity"] != SeverityLevel.NONE,
                x["confidence"],
                x["severity"] == SeverityLevel.SEVERE
            ),
            reverse=True
        )
        
        # If focus areas specified, prioritize those
        if focus_areas:
            focused = [c for c in priority_conditions if c["condition_type"] in focus_areas]
            unfocused = [c for c in priority_conditions if c["condition_type"] not in focus_areas]
            priority_conditions = focused + unfocused
        
        # Limit to top 3 conditions to avoid overwhelming the user
        return priority_conditions[:3]
    
    def _recommend_products(
        self,
        priority_conditions: List[Dict],
        user_profile: Optional[Dict[str, Any]],
        budget_preference: Optional[str],
        routine_complexity: str
    ) -> List[RecommendedProduct]:
        """Recommend products based on conditions and preferences"""
        recommended_products = []
        template = self._get_routine_template(routine_complexity)
        
        # Always include basic products
        for category in template["required_categories"]:
            products = self._get_products_for_category(category, priority_conditions)
            if products:
                best_product = self._select_best_product(
                    products, user_profile, budget_preference
                )
                if best_product:
                    recommended_products.append(best_product)
        
        # Add targeted treatments based on conditions
        actives_added = 0
        for condition in priority_conditions:
            if actives_added >= template["max_actives"]:
                break
                
            treatment_products = self._get_targeted_treatments(condition)
            if treatment_products:
                best_treatment = self._select_best_product(
                    treatment_products, user_profile, budget_preference
                )
                if best_treatment and best_treatment not in recommended_products:
                    recommended_products.append(best_treatment)
                    actives_added += 1
        
        return recommended_products[:template["max_products"]]
    
    def _get_routine_template(self, complexity: str) -> Dict:
        """Get routine template based on complexity level"""
        return self.routine_templates.get(complexity, self.routine_templates["beginner"])
    
    def _get_products_for_category(
        self,
        category: ProductCategory,
        conditions: List[Dict]
    ) -> List[RecommendedProduct]:
        """Get products from a specific category that address the conditions"""
        products = self.product_database.get(category.value, [])
        
        # Filter products that target the conditions
        relevant_products = []
        for product in products:
            condition_types = [c["condition_type"] for c in conditions]
            if any(target in condition_types for target in product.target_conditions):
                relevant_products.append(product)
        
        # If no specific matches, return general products for the category
        return relevant_products if relevant_products else products
    
    def _get_targeted_treatments(self, condition: Dict) -> List[RecommendedProduct]:
        """Get targeted treatment products for a specific condition"""
        treatment_products = self.product_database.get(ProductCategory.TREATMENT.value, [])
        serum_products = self.product_database.get(ProductCategory.SERUM.value, [])
        
        all_treatments = treatment_products + serum_products
        
        # Filter for products that target this specific condition
        targeted = [
            product for product in all_treatments
            if condition["condition_type"] in product.target_conditions
        ]
        
        return targeted
    
    def _select_best_product(
        self,
        products: List[RecommendedProduct],
        user_profile: Optional[Dict[str, Any]],
        budget_preference: Optional[str]
    ) -> Optional[RecommendedProduct]:
        """Select the best product from a list based on user preferences"""
        if not products:
            return None
        
        # Score products based on various factors
        scored_products = []
        for product in products:
            score = product.recommendation_confidence
            
            # Adjust for personalization if user profile available
            if user_profile:
                score += product.personalization_score * 0.2
            
            # Adjust for budget preference
            if budget_preference:
                budget_score = self._calculate_budget_score(product, budget_preference)
                score += budget_score * 0.1
            
            scored_products.append((product, score))
        
        # Return product with highest score
        best_product = max(scored_products, key=lambda x: x[1])
        return best_product[0]
    
    def _calculate_budget_score(self, product: RecommendedProduct, budget_preference: str) -> float:
        """Calculate budget compatibility score"""
        # Extract price range (simplified)
        price_range = product.price_range or "$0-50"
        
        # Simple budget scoring logic
        if budget_preference == "low":
            return 1.0 if "$" in price_range and not "30" in price_range else 0.5
        elif budget_preference == "high":
            return 1.0 if "30" in price_range or "40" in price_range else 0.8
        else:  # medium
            return 0.9
    
    def _create_skincare_routine(
        self,
        products: List[RecommendedProduct],
        complexity: str
    ) -> SkincareRoutine:
        """Create organized skincare routine from recommended products"""
        morning_routine = []
        evening_routine = []
        weekly_treatments = []
        
        # Sort products by application order
        sorted_products = sorted(products, key=lambda x: x.application_order)
        
        for product in sorted_products:
            if product.time_of_day == TimeOfDay.MORNING:
                morning_routine.append(product)
            elif product.time_of_day == TimeOfDay.EVENING:
                evening_routine.append(product)
            elif product.time_of_day == TimeOfDay.BOTH:
                morning_routine.append(product)
                evening_routine.append(product)
            
            # Add to weekly treatments if infrequent usage
            if "week" in product.usage_frequency or "times per week" in product.usage_frequency:
                weekly_treatments.append(product)
        
        return SkincareRoutine(
            routine_id=str(uuid.uuid4()),
            morning_routine=morning_routine,
            evening_routine=evening_routine,
            weekly_treatments=weekly_treatments,
            difficulty_level=complexity,
            estimated_cost=self._estimate_routine_cost(products),
            time_commitment=self._estimate_time_commitment(products, complexity)
        )
    
    def _estimate_routine_cost(self, products: List[RecommendedProduct]) -> str:
        """Estimate monthly cost of routine"""
        # Simplified cost estimation
        total_products = len(products)
        if total_products <= 3:
            return "$30-60/month"
        elif total_products <= 5:
            return "$50-100/month"
        else:
            return "$80-150/month"
    
    def _estimate_time_commitment(self, products: List[RecommendedProduct], complexity: str) -> str:
        """Estimate daily time commitment"""
        if complexity == "beginner":
            return "3-5 minutes"
        elif complexity == "intermediate":
            return "5-8 minutes"
        else:
            return "8-12 minutes"
    
    def _generate_general_advice(
        self,
        priority_conditions: List[Dict],
        user_profile: Optional[Dict[str, Any]]
    ) -> GeneralAdvice:
        """Generate general skincare advice based on conditions"""
        lifestyle_tips = [
            "Stay hydrated by drinking plenty of water",
            "Get adequate sleep for skin repair and renewal",
            "Manage stress through relaxation techniques",
            "Avoid touching your face frequently"
        ]
        
        dietary_suggestions = [
            "Include antioxidant-rich foods in your diet",
            "Consider reducing dairy if you have acne-prone skin",
            "Limit high-glycemic foods that may trigger breakouts"
        ]
        
        habits_to_avoid = [
            "Don't over-wash your face",
            "Avoid picking at blemishes",
            "Don't skip sunscreen, even on cloudy days"
        ]
        
        # Add condition-specific advice
        condition_types = [c["condition_type"] for c in priority_conditions]
        
        if SkinConditionType.ACNE in condition_types:
            habits_to_avoid.append("Avoid heavy, pore-clogging products")
            dietary_suggestions.append("Consider probiotics for gut health")
        
        if SkinConditionType.WRINKLES in condition_types:
            lifestyle_tips.append("Use a silk pillowcase to reduce friction")
            habits_to_avoid.append("Don't sleep on your stomach")
        
        if SkinConditionType.DRYNESS in condition_types:
            lifestyle_tips.append("Use a humidifier in dry environments")
            habits_to_avoid.append("Avoid hot showers that strip natural oils")
        
        return GeneralAdvice(
            lifestyle_tips=lifestyle_tips,
            dietary_suggestions=dietary_suggestions,
            habits_to_avoid=habits_to_avoid,
            when_to_see_dermatologist="If conditions worsen or don't improve after 8-12 weeks"
        )
    
    def _format_priority_conditions(self, conditions: List[Dict]) -> List[Dict[str, Any]]:
        """Format priority conditions for response"""
        formatted = []
        for condition in conditions:
            formatted.append({
                "condition": condition["condition_type"].value,
                "severity": condition["severity"].value,
                "confidence": condition["confidence"],
                "treatment_priority": "high" if condition["severity"] == SeverityLevel.SEVERE else "medium"
            })
        return formatted
    
    def _estimate_improvement_timeline(self, conditions: List[Dict]) -> str:
        """Estimate when improvements might be visible"""
        # Different conditions have different improvement timelines
        timelines = []
        
        for condition in conditions:
            if condition["condition_type"] == SkinConditionType.ACNE:
                timelines.append("6-8 weeks for acne improvement")
            elif condition["condition_type"] == SkinConditionType.DARK_SPOTS:
                timelines.append("8-12 weeks for dark spot fading")
            elif condition["condition_type"] == SkinConditionType.WRINKLES:
                timelines.append("12-16 weeks for anti-aging results")
            elif condition["condition_type"] == SkinConditionType.OILINESS:
                timelines.append("2-4 weeks for oil control")
            elif condition["condition_type"] == SkinConditionType.DRYNESS:
                timelines.append("1-2 weeks for hydration improvement")
        
        if timelines:
            return "; ".join(timelines)
        return "4-8 weeks for general skin improvement"
    
    def _calculate_recommendation_confidence(
        self,
        conditions: List[Dict],
        has_user_profile: bool,
        complexity: str
    ) -> float:
        """Calculate overall confidence in recommendations"""
        base_confidence = 0.8
        
        # Higher confidence with more severe/confident conditions
        if conditions:
            avg_condition_confidence = sum(c["confidence"] for c in conditions) / len(conditions)
            base_confidence += (avg_condition_confidence - 0.7) * 0.2
        
        # Higher confidence with user profile
        if has_user_profile:
            base_confidence += 0.1
        
        # Adjust for complexity
        complexity_modifier = {
            "beginner": 0.05,
            "intermediate": 0.0,
            "advanced": -0.05
        }
        base_confidence += complexity_modifier.get(complexity, 0)
        
        return min(1.0, max(0.0, base_confidence))