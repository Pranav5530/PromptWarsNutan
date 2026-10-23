import pytest
from datetime import datetime, timezone, timedelta
from app.rules.fssai_rules import FSSAIRuleEngine
from app.schemas.foodloop import FoodListingCreate, FoodCategory, DietaryType, StorageCondition, SafetyVerdict


def create_listing(hours_ago: float, temp_c: float, storage: StorageCondition) -> FoodListingCreate:
    prep_time = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    return FoodListingCreate(
        donor_id="donor-1",
        donor_name="Taj Kitchen",
        food_name="Dal Makhani & Jeera Rice",
        category=FoodCategory.COOKED_MEAL,
        estimated_kg=20.0,
        meal_count=40,
        dietary_type=DietaryType.VEGETARIAN,
        allergens=["dairy"],
        prep_timestamp=prep_time,
        storage_condition=storage,
        ambient_temp_celsius=temp_c,
        donor_latitude=12.9716,
        donor_longitude=77.5946,
        donor_address_masked="MG Road, Bengaluru"
    )


def test_fssai_safe_listing():
    # Cooked 1 hour ago, room temp 26C -> Safe
    listing = create_listing(hours_ago=1.0, temp_c=26.0, storage=StorageCondition.ROOM_TEMP)
    verdict, violations, window, passed = FSSAIRuleEngine.evaluate(listing)
    assert verdict == SafetyVerdict.SAFE
    assert len(violations) == 0
    assert window == 4.0
    assert passed is True


def test_fssai_rejected_expired_holding():
    # Cooked 5.5 hours ago, room temp -> REJECTED (exceeds 4 hr limit)
    listing = create_listing(hours_ago=5.5, temp_c=28.0, storage=StorageCondition.ROOM_TEMP)
    verdict, violations, window, passed = FSSAIRuleEngine.evaluate(listing)
    assert verdict == SafetyVerdict.REJECTED
    assert len(violations) > 0
    assert "exceeds maximum allowed safe window" in violations[0]
    assert passed is False


def test_fssai_rejected_high_ambient_heat():
    # Cooked 2.5 hours ago in extreme heat (>32C, 35C) -> REJECTED (exceeds 2.0 hr limit)
    listing = create_listing(hours_ago=2.5, temp_c=35.0, storage=StorageCondition.ROOM_TEMP)
    verdict, violations, window, passed = FSSAIRuleEngine.evaluate(listing)
    assert verdict == SafetyVerdict.REJECTED
    assert window == 2.0
    assert passed is False


def test_fssai_risky_narrow_window():
    # Cooked 3.5 hours ago, room temp (allowed is 4.0h) -> RISKY (less than 45 min left)
    listing = create_listing(hours_ago=3.5, temp_c=27.0, storage=StorageCondition.ROOM_TEMP)
    verdict, violations, window, passed = FSSAIRuleEngine.evaluate(listing)
    assert verdict == SafetyVerdict.RISKY
    assert "critically narrow" in violations[0]
