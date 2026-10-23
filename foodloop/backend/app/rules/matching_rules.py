import math
from typing import Dict, Any, List
from app.schemas.foodloop import MatchCandidate


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two GPS coordinates in kilometers.
    """
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2.0) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


class MatchingScorer:
    """
    Multi-objective scoring engine for matching food surplus to nearby NGOs.
    Formula: Score = 0.35*Distance + 0.35*Capacity + 0.20*Dietary + 0.10*Urgency
    """
    @staticmethod
    def calculate_score(
        distance_km: float,
        listing_meals: int,
        ngo_capacity_needed: int,
        listing_dietary: str,
        ngo_dietary_policy: str,
        urgency_hours_left: float,
        max_radius_km: float = 5.0
    ) -> float:
        # 1. Distance Score (Linear decay, 0 at >= 5 km)
        if distance_km > max_radius_km:
            dist_score = 0.0
        else:
            dist_score = max(0.0, 1.0 - (distance_km / max_radius_km))

        # 2. Capacity Score (How closely capacity matches meal count)
        if ngo_capacity_needed <= 0:
            cap_score = 0.1
        else:
            ratio = min(listing_meals, ngo_capacity_needed) / max(listing_meals, ngo_capacity_needed)
            cap_score = ratio

        # 3. Dietary Compatibility Score
        if ngo_dietary_policy == "veg_only":
            dietary_score = 1.0 if listing_dietary in ["vegetarian", "vegan", "jain"] else 0.0
        elif ngo_dietary_policy == "jain":
            dietary_score = 1.0 if listing_dietary == "jain" else 0.0
        else: # "all"
            dietary_score = 1.0

        # If dietary policy strictly violated (e.g. non-veg to veg_only shelter), entire match is ineligible
        if dietary_score == 0.0:
            return 0.0

        # 4. Urgency Score (High score if safe window is closing rapidly)
        if urgency_hours_left <= 1.0:
            urgency_score = 1.0
        elif urgency_hours_left <= 2.5:
            urgency_score = 0.8
        else:
            urgency_score = 0.5

        # Weighted composite score
        composite = (
            (0.35 * dist_score)
            + (0.35 * cap_score)
            + (0.20 * dietary_score)
            + (0.10 * urgency_score)
        )
        return round(min(1.0, max(0.0, composite)), 4)
