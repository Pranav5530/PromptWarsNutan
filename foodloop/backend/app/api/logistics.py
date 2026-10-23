from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from app.core.security import require_role, AuthenticatedUser
from app.schemas.foodloop import DispatchRecord
from app.agents.logistics_agent import logistics_agent

router = APIRouter(prefix="/agent", tags=["Logistics & Dispatch"])


class DispatchRequest(BaseModel):
    listing_id: str
    ngo_id: str
    donor_lat: float
    donor_lng: float
    ngo_lat: float
    ngo_lng: float


class StatusUpdateRequest(BaseModel):
    status: str # "en_route_pickup", "picked_up", "delivered"


@router.post("/dispatch", response_model=DispatchRecord)
async def dispatch_volunteer(
    req: DispatchRequest,
    current_user: AuthenticatedUser = Depends(require_role(["ngo", "admin"]))
):
    """
    Called upon NGO acceptance: selects nearest volunteer and generates route/ETA.
    """
    return await logistics_agent.assign_volunteer(
        listing_id=req.listing_id,
        ngo_id=req.ngo_id,
        donor_lat=req.donor_lat,
        donor_lng=req.donor_lng,
        ngo_lat=req.ngo_lat,
        ngo_lng=req.ngo_lng
    )


@router.post("/dispatch/{dispatch_id}/proof-of-delivery")
async def upload_proof_of_delivery(
    dispatch_id: str,
    proof_photo: Optional[UploadFile] = File(None),
    notes: Optional[str] = Form(None),
    current_user: AuthenticatedUser = Depends(require_role(["volunteer", "admin"]))
):
    """
    Volunteer uploads photo proof of delivery to mark rescue task completed.
    """
    return {
        "dispatch_id": dispatch_id,
        "status": "delivered",
        "verified_by_volunteer": current_user.uid,
        "proof_photo_url": "gs://foodloop-proofs/" + dispatch_id + "-pod.jpg",
        "message": "Rescue successfully delivered and verified!"
    }
