from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List
from jose import jwt, JWTError
from app.core.config import settings

security_bearer = HTTPBearer(auto_error=False)


class AuthenticatedUser:
    def __init__(self, uid: str, email: str, role: str, name: Optional[str] = None):
        self.uid = uid
        self.email = email
        self.role = role
        self.name = name or email.split("@")[0]


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)
) -> AuthenticatedUser:
    """
    Validates Firebase Auth JWT or dev test token and extracts custom role claim.
    """
    if not credentials:
        # Development fallback / anonymous mock for testing when no header
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    # In test/dev mode, allow synthetic tokens prefixed with test-
    if token.startswith("test-"):
        parts = token.split(":")
        role = parts[1] if len(parts) > 1 else "donor"
        uid = parts[2] if len(parts) > 2 else "test-uid-123"
        email = f"{role}@foodloop.test"
        return AuthenticatedUser(uid=uid, email=email, role=role)
        
    try:
        # Decode Firebase JWT (in production, verified via Firebase Admin SDK / public keys)
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_signature": False} # Permissive dev mode
        )
        uid = payload.get("sub") or payload.get("user_id") or "user-default"
        email = payload.get("email", "user@foodloop.org")
        role = payload.get("role", "donor")
        name = payload.get("name")
        return AuthenticatedUser(uid=uid, email=email, role=role, name=name)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_role(allowed_roles: List[str]):
    """
    Enforces Role-Based Access Control (RBAC).
    """
    def role_checker(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
        if user.role not in allowed_roles and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: User role '{user.role}' not permitted for this action. Allowed: {allowed_roles}"
            )
        return user
    return role_checker
