import json
import os
import pytest
from datetime import datetime, timezone, timedelta
from app.rules.fssai_rules import FSSAIRuleEngine
from app.schemas.foodloop import FoodListingCreate, FoodCategory, DietaryType, StorageCondition, SafetyVerdict
from app.core.guardrails import sanitize_untrusted_input


def load_eval_dataset():
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, "data", "eval_listings.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_30_sample_evaluation_suite():
    dataset = load_eval_dataset()
    assert len(dataset) == 30, f"Expected 30 evaluation items, got {len(dataset)}"

    correct_predictions = 0
    zero_tolerance_violations = 0
    now = datetime.now(timezone.utc)

    for item in dataset:
        prep_time = now - timedelta(hours=item["prep_hours_ago"])
        storage_map = {
            "room_temp": StorageCondition.ROOM_TEMP,
            "hot_held": StorageCondition.HOT_HELD,
            "refrigerated": StorageCondition.REFRIGERATED
        }
        category_map = {
            "cooked_meal": FoodCategory.COOKED_MEAL,
            "bakery": FoodCategory.BAKERY,
            "raw_produce": FoodCategory.RAW_PRODUCE,
            "packaged": FoodCategory.PACKAGED
        }

        listing = FoodListingCreate(
            donor_id=f"donor-{item['id']}",
            donor_name="Evaluation Donor",
            food_name=item["name"],
            category=category_map.get(item["category"], FoodCategory.COOKED_MEAL),
            estimated_kg=15.0,
            meal_count=30,
            dietary_type=DietaryType.VEGETARIAN if item["dietary"] == "vegetarian" else DietaryType.NON_VEGETARIAN,
            allergens=item.get("allergens", []),
            prep_timestamp=prep_time,
            storage_condition=storage_map.get(item["storage"], StorageCondition.ROOM_TEMP),
            ambient_temp_celsius=item["temp_c"],
            donor_latitude=12.9716,
            donor_longitude=77.5946,
            donor_address_masked="Test Location"
        )

        # Check prompt injection guard for adversarial items
        if item.get("is_adversarial"):
            _, is_suspicious = sanitize_untrusted_input(item["name"])
            assert is_suspicious is True, f"Adversarial item {item['id']} failed to trigger guardrail"

        # Deterministic FSSAI rule evaluation
        verdict, violations, window, passed = FSSAIRuleEngine.evaluate(listing)

        expected = item["expected_verdict"]

        # ZERO TOLERANCE: If item is expected Rejected, it must NEVER be marked Safe
        if expected == "Rejected" and verdict == SafetyVerdict.SAFE:
            zero_tolerance_violations += 1

        if verdict.value == expected:
            correct_predictions += 1

    accuracy = (correct_predictions / len(dataset)) * 100.0

    # Hard assertions per FoodLoop Constitution & Spec Criteria
    assert zero_tolerance_violations == 0, f"SAFETY BREACH: {zero_tolerance_violations} unsafe items auto-approved!"
    assert accuracy >= 90.0, f"Evaluation accuracy was {accuracy:.1f}%, target is >= 90.0%"
    print(f"\n[FoodLoop Benchmark] 30-Sample Evaluation Suite Passed! Accuracy: {accuracy:.1f}% | Unsafe Auto-Approved: 0")
