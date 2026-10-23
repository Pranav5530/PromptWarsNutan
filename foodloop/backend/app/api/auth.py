from fastapi import APIRouter, Depends
from app.core.security import get_current_user, AuthenticatedUser

router = APIRouter(prefix="/auth", tags=["Authentication & Roles"])


@router.get("/me")
async def get_my_profile(current_user: AuthenticatedUser = Depends(get_current_user)):
    """
    Returns authenticated user profile and active role claim.
    """
    return {
        "uid": current_user.uid,
        "email": current_user.email,
        "role": current_user.role,
        "display_name": current_user.name
    }
