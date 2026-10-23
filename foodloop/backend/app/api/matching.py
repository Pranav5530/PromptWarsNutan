from fastapi import APIRouter, Depends
from app.core.security import require_role, AuthenticatedUser
from app.schemas.foodloop import FoodListingCreate, MatchResult
from app.agents.matching_agent import matching_agent

router = APIRouter(prefix="/agent", tags=["Matching Agent"])


@router.post("/match", response_model=MatchResult)
async def rank_matching_ngos(
    listing: FoodListingCreate,
    current_user: AuthenticatedUser = Depends(require_role(["donor", "ngo", "admin"]))
):
    """
    Ranks nearby NGOs (<5km) based on distance, capacity deficit, dietary compatibility, and urgency.
    """
    return await matching_agent.match_listing(listing, listing_id="listing-" + listing.donor_id[:8])
