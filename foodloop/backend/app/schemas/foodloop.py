from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    DONOR = "donor"
    NGO = "ngo"
    VOLUNTEER = "volunteer"
    ADMIN = "admin"


class FoodCategory(str, Enum):
    COOKED_MEAL = "cooked_meal"
    BAKERY = "bakery"
    RAW_PRODUCE = "raw_produce"
    PACKAGED = "packaged"


class DietaryType(str, Enum):
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    NON_VEGETARIAN = "non_vegetarian"
    JAIN = "jain"


class StorageCondition(str, Enum):
    HOT_HELD = "hot_held"
    ROOM_TEMP = "room_temp"
    REFRIGERATED = "refrigerated"


class SafetyVerdict(str, Enum):
    SAFE = "Safe"
    RISKY = "Risky"
    REJECTED = "Rejected"


class ListingStatus(str, Enum):
    DRAFT = "draft"
    EVALUATING = "evaluating"
    SAFE = "safe"
    RISKY = "risky"
    REJECTED = "rejected"
    MATCHING = "matching"
    MATCHED = "matched"
    DISPATCHING = "dispatching"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    EXPIRED = "expired"


# 1. Intake Schemas
class FoodIntakeDraft(BaseModel):
    food_name: str = Field(description="Recognized name of dish or food item")
    category: FoodCategory = Field(default=FoodCategory.COOKED_MEAL)
    estimated_kg: float = Field(ge=0.1, le=5000.0, description="Estimated total weight in kilograms")
    meal_count: int = Field(ge=1, description="Estimated number of meal portions")
    dietary_type: DietaryType = Field(default=DietaryType.VEGETARIAN)
    allergens: List[str] = Field(default_factory=list, description="List of recognized allergens, e.g. dairy, nuts")
    safe_consume_hours: int = Field(ge=1, le=48, default=4, description="Recommended safe consumption window in hours")
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.95)
    notes: Optional[str] = None


class FoodListingCreate(BaseModel):
    donor_id: str
    donor_name: str
    photo_url: Optional[str] = None
    food_name: str
    category: FoodCategory = FoodCategory.COOKED_MEAL
    estimated_kg: float
    meal_count: int
    dietary_type: DietaryType = DietaryType.VEGETARIAN
    allergens: List[str] = Field(default_factory=list)
    prep_timestamp: datetime
    storage_condition: StorageCondition = StorageCondition.ROOM_TEMP
    ambient_temp_celsius: float = 28.0
    donor_latitude: float
    donor_longitude: float
    donor_address_masked: str


class SafetyEvaluation(BaseModel):
    listing_id: str
    verdict: SafetyVerdict
    rule_violations: List[str] = Field(default_factory=list)
    ai_explanation: str
    fssai_window_hours: float
    deterministic_checks_passed: bool
    requires_donor_override: bool = False
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)


class MatchCandidate(BaseModel):
    ngo_id: str
    ngo_name: str
    score: float = Field(ge=0.0, le=1.0)
    distance_km: float
    capacity_needed: int
    dietary_compatible: bool
    reasoning: str


class MatchResult(BaseModel):
    listing_id: str
    ranked_candidates: List[MatchCandidate]
    selected_ngo: Optional[MatchCandidate] = None
    match_latency_sec: float
    matched_at: datetime = Field(default_factory=datetime.utcnow)


class DispatchRecord(BaseModel):
    dispatch_id: str
    listing_id: str
    ngo_id: str
    volunteer_id: str
    volunteer_name: str
    volunteer_phone: str
    eta_minutes: int
    directions_url: str
    status: str = "assigned"
    proof_photo_url: Optional[str] = None
    assigned_at: datetime = Field(default_factory=datetime.utcnow)


class ImpactMetrics(BaseModel):
    total_kg_rescued: float = 0.0
    total_meals_served: int = 0
    co2_saved_kg: float = 0.0
    avg_match_time_sec: float = 0.0
    active_rescues: int = 0
    success_rate_percent: float = 100.0


class SurplusHotspot(BaseModel):
    area_name: str
    city: str
    peak_hour: str
    predicted_surplus_kg: float
    active_donor_count: int
