from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Optional
from app.core.security import require_role, AuthenticatedUser
from app.schemas.foodloop import FoodIntakeDraft
from app.agents.intake_agent import intake_agent

router = APIRouter(prefix="/agent", tags=["Intake Agent"])


@router.post("/intake", response_model=FoodIntakeDraft)
async def process_food_intake(
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    donor_notes: Optional[str] = Form(None),
    current_user: AuthenticatedUser = Depends(require_role(["donor", "admin"]))
):
    """
    Multimodal intake endpoint for donors. Accepts photo or voice note and auto-extracts
    food name, estimated kg, meal count, dietary type, allergens, and safe-consume window.
    """
    image_bytes = await image.read() if image else None
    audio_bytes = await audio.read() if audio else None
    
    draft = await intake_agent.process_intake(
        image_bytes=image_bytes,
        audio_bytes=audio_bytes,
        donor_notes=donor_notes
    )
    return draft
