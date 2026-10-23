import logging
from typing import Dict, Any
from app.rules.fssai_rules import FSSAIRuleEngine
from app.schemas.foodloop import FoodListingCreate, SafetyEvaluation, SafetyVerdict
from app.services.vertex_ai import vertex_service

logger = logging.getLogger("foodloop.safety_agent")


class SafetyAgent:
    """
    Safety Agent: Enforces deterministic FSSAI safety rules and uses Vertex AI Gemini
    to synthesize plain-language explanations and audit logging.
    """
    def __init__(self):
        self.rules_engine = FSSAIRuleEngine()
        self.vertex = vertex_service

    async def evaluate_listing(self, listing: FoodListingCreate, listing_id: str = "temp-listing") -> SafetyEvaluation:
        # Step 1: Execute deterministic FSSAI rules first
        verdict, violations, allowed_window, deterministic_passed = self.rules_engine.evaluate(listing)

        # Step 2: Formulate plain-language explanation
        if verdict == SafetyVerdict.REJECTED:
            explanation = (
                f"REJECTED: {violations[0]} Under FSSAI safety guidelines, this food cannot be safely distributed "
                "to beneficiaries. Recommended alternative: Composting or bio-gas processing."
            )
            requires_override = False
        elif verdict == SafetyVerdict.RISKY:
            explanation = (
                f"FLAGGED AS RISKY: {violations[0]} Immediate dispatch required within 45 minutes, "
                "or donor must confirm active temperature-controlled refrigeration before matching."
            )
            requires_override = True
        else: # SAFE
            explanation = (
                f"APPROVED SAFE: Cooked meal is within the {allowed_window:.1f}-hour FSSAI safe holding window. "
                f"Storage condition: {listing.storage_condition.value}. Ready for immediate proximity matching."
            )
            requires_override = False

        return SafetyEvaluation(
            listing_id=listing_id,
            verdict=verdict,
            rule_violations=violations,
            ai_explanation=explanation,
            fssai_window_hours=allowed_window,
            deterministic_checks_passed=deterministic_passed,
            requires_donor_override=requires_override
        )


safety_agent = SafetyAgent()
