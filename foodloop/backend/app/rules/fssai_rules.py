from datetime import datetime, timezone
from typing import List, Tuple
from app.schemas.foodloop import FoodListingCreate, StorageCondition, SafetyVerdict, FoodCategory
from app.core.config import settings


class FSSAIRuleEngine:
    """
    Deterministic Food Safety and Standards Authority of India (FSSAI) rule engine.
    Zero-tolerance deterministic verification.
    """

    @staticmethod
    def evaluate(listing: FoodListingCreate) -> Tuple[SafetyVerdict, List[str], float, bool]:
        """
        Evaluates listing against deterministic safety limits.
        Returns (verdict, list_of_violations, allowed_window_hours, deterministic_passed).
        """
        violations: List[str] = []
        now = datetime.now(timezone.utc)
        
        # Ensure timezone-aware comparison
        prep_time = listing.prep_timestamp
        if prep_time.tzinfo is None:
            prep_time = prep_time.replace(tzinfo=timezone.utc)

        elapsed_hours = (now - prep_time).total_seconds() / 3600.0
        
        # 1. Determine allowed safe consumption window based on storage & ambient temperature
        if listing.category == FoodCategory.BAKERY or listing.category == FoodCategory.PACKAGED:
            allowed_window = 48.0
        elif listing.storage_condition == StorageCondition.REFRIGERATED:
            allowed_window = 24.0
        elif listing.storage_condition == StorageCondition.HOT_HELD:
            allowed_window = 6.0
        else: # ROOM_TEMP
            if listing.ambient_temp_celsius >= settings.HIGH_HEAT_TEMP_THRESHOLD_C:
                allowed_window = settings.FSSAI_HIGH_HEAT_MAX_HOURS # 2.0 hrs in extreme heat (>32°C)
            else:
                allowed_window = settings.FSSAI_MAX_AMBIENT_HOURS # 4.0 hrs standard ambient

        # 2. Check elapsed holding time against allowed window
        if elapsed_hours > allowed_window:
            violations.append(
                f"Elapsed time since preparation ({elapsed_hours:.1f}h) exceeds maximum allowed safe window ({allowed_window:.1f}h) under {listing.storage_condition.value}."
            )
            return SafetyVerdict.REJECTED, violations, allowed_window, False

        # 3. Check borderline conditions
        if elapsed_hours >= (allowed_window - 0.75):
            # Less than 45 minutes remaining before expiry
            violations.append(
                f"Perishable window critically narrow: only {max(0, allowed_window - elapsed_hours):.1f}h remaining before safe consumption limit."
            )
            return SafetyVerdict.RISKY, violations, allowed_window, True

        # 4. Check high-risk perishables stored at room temperature in warm climate
        if (
            listing.ambient_temp_celsius >= 30.0
            and listing.storage_condition == StorageCondition.ROOM_TEMP
            and elapsed_hours > 2.5
        ):
            violations.append(
                "Cooked high-moisture meal at ambient room temperature in high heat (>30°C) approaching microbial growth threshold."
            )
            return SafetyVerdict.RISKY, violations, allowed_window, True

        # All deterministic checks passed
        return SafetyVerdict.SAFE, [], allowed_window, True
