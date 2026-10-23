import pytest
from datetime import datetime, timezone
from app.schemas.foodloop import FoodListingCreate, FoodCategory, DietaryType, StorageCondition
from app.agents.matching_agent import MatchingAgent


@pytest.mark.asyncio
async def test_matching_ranking_and_distance_cutoff():
    agent = MatchingAgent()
    listing = FoodListingCreate(
        donor_id="donor-bengaluru-1",
        donor_name="Indiranagar Club",
        food_name="Paneer Butter Masala & Roti",
        category=FoodCategory.COOKED_MEAL,
        estimated_kg=25.0,
        meal_count=50,
        dietary_type=DietaryType.VEGETARIAN,
        allergens=["dairy", "gluten"],
        prep_timestamp=datetime.now(timezone.utc),
        storage_condition=StorageCondition.ROOM_TEMP,
        ambient_temp_celsius=26.0,
        donor_latitude=12.9716,
        donor_longitude=77.5946,
        donor_address_masked="Indiranagar 100ft Road"
    )

    result = await agent.match_listing(listing, listing_id="list-test-01")
    assert len(result.ranked_candidates) > 0
    # Must NOT include the NGO that is > 15 km away
    ngo_ids = [c.ngo_id for c in result.ranked_candidates]
    assert "ngo-far-004" not in ngo_ids
    assert result.selected_ngo is not None
    assert result.selected_ngo.score > 0.60
    assert result.match_latency_sec < 1.0 # SLA is < 60s, here < 1s


@pytest.mark.asyncio
async def test_matching_dietary_filtering():
    agent = MatchingAgent()
    # Non-vegetarian food should not be matched to a veg-only shelter
    listing = FoodListingCreate(
        donor_id="donor-bengaluru-2",
        donor_name="Kabab Corner",
        food_name="Chicken Biryani",
        category=FoodCategory.COOKED_MEAL,
        estimated_kg=30.0,
        meal_count=60,
        dietary_type=DietaryType.NON_VEGETARIAN,
        allergens=[],
        prep_timestamp=datetime.now(timezone.utc),
        storage_condition=StorageCondition.HOT_HELD,
        ambient_temp_celsius=26.0,
        donor_latitude=12.9716,
        donor_longitude=77.5946,
        donor_address_masked="MG Road"
    )

    result = await agent.match_listing(listing, listing_id="list-test-02")
    for cand in result.ranked_candidates:
        # None of the ranked candidates should be a veg_only shelter
        assert cand.ngo_id != "ngo-asha-001"
        assert cand.ngo_id != "ngo-annapurna-003"
    # City Care Foundation accepts 'all' dietary types
    assert result.selected_ngo.ngo_id == "ngo-citycare-002"
