from fastapi import APIRouter, Depends
from app.core.security import require_role, AuthenticatedUser
from app.schemas.foodloop import FoodListingCreate, SafetyEvaluation
from app.agents.safety_agent import safety_agent

router = APIRouter(prefix="/agent", tags=["Safety Agent"])


@router.post("/safety-check", response_model=SafetyEvaluation)
async def check_food_safety(
    listing: FoodListingCreate,
    current_user: AuthenticatedUser = Depends(require_role(["donor", "ngo", "admin"]))
):
    """
    Evaluates food safety using deterministic FSSAI rules and Gemini reasoning.
    Returns Safe, Risky, or Rejected with clear plain-language explanation.
    """
    return await safety_agent.evaluate_listing(listing, listing_id="listing-" + listing.donor_id[:8])
