import time
from typing import List, Dict, Any
from app.rules.matching_rules import haversine_distance_km, MatchingScorer
from app.schemas.foodloop import MatchCandidate, MatchResult, FoodListingCreate

# Default verified NGO shelters in Bengaluru/urban hub for matching
DEFAULT_NGOS = [
    {
        "id": "ngo-asha-001",
        "name": "Asha Shelter Home",
        "latitude": 12.9750,
        "longitude": 77.6000,
        "capacity_needed": 50,
        "dietary_policy": "veg_only",
        "contact_phone": "+91-98765-11001"
    },
    {
        "id": "ngo-citycare-002",
        "name": "City Care Foundation",
        "latitude": 12.9900,
        "longitude": 77.6150,
        "capacity_needed": 100,
        "dietary_policy": "all",
        "contact_phone": "+91-98765-22002"
    },
    {
        "id": "ngo-annapurna-003",
        "name": "Annapurna Seva Trust",
        "latitude": 12.9600,
        "longitude": 77.5800,
        "capacity_needed": 35,
        "dietary_policy": "veg_only",
        "contact_phone": "+91-98765-33003"
    },
    {
        "id": "ngo-far-004",
        "name": "Suburban Hope Center",
        "latitude": 13.1000,
        "longitude": 77.8000, # >15 km away
        "capacity_needed": 200,
        "dietary_policy": "all",
        "contact_phone": "+91-98765-44004"
    }
]


class MatchingAgent:
    """
    Matching Agent: Performs proximity calculation, multi-objective ranking,
    and rationale synthesis for surplus food rescue.
    """
    def __init__(self, ngos: List[Dict[str, Any]] = None):
        self.ngos = ngos or DEFAULT_NGOS
        self.scorer = MatchingScorer()

    async def match_listing(
        self,
        listing: FoodListingCreate,
        listing_id: str,
        urgency_hours: float = 3.0
    ) -> MatchResult:
        start_time = time.time()
        candidates: List[MatchCandidate] = []

        for ngo in self.ngos:
            distance = haversine_distance_km(
                listing.donor_latitude,
                listing.donor_longitude,
                ngo["latitude"],
                ngo["longitude"]
            )

            # Skip NGOs beyond 5 km limit
            if distance > 5.0:
                continue

            score = self.scorer.calculate_score(
                distance_km=distance,
                listing_meals=listing.meal_count,
                ngo_capacity_needed=ngo["capacity_needed"],
                listing_dietary=listing.dietary_type.value,
                ngo_dietary_policy=ngo["dietary_policy"],
                urgency_hours_left=urgency_hours,
                max_radius_km=5.0
            )

            # Ineligible dietary match gives 0.0
            if score == 0.0:
                continue

            reasoning = (
                f"{ngo['name']} is located {distance:.2f} km away (sub-5km radius). "
                f"Needs {ngo['capacity_needed']} meals (listing has {listing.meal_count}), "
                f"with 100% {ngo['dietary_policy']} policy alignment."
            )

            candidates.append(
                MatchCandidate(
                    ngo_id=ngo["id"],
                    ngo_name=ngo["name"],
                    score=score,
                    distance_km=round(distance, 2),
                    capacity_needed=ngo["capacity_needed"],
                    dietary_compatible=True,
                    reasoning=reasoning
                )
            )

        # Sort candidates descending by match score
        candidates.sort(key=lambda c: c.score, reverse=True)
        top_ngo = candidates[0] if candidates else None
        elapsed_sec = round(time.time() - start_time, 3)

        return MatchResult(
            listing_id=listing_id,
            ranked_candidates=candidates,
            selected_ngo=top_ngo,
            match_latency_sec=elapsed_sec
        )


matching_agent = MatchingAgent()
