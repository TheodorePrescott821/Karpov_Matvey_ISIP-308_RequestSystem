"""FastAPI dependencies for authentication and authorization."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from request_system.application.services.auth_service import AuthService


security = HTTPBearer()


class CurrentUser:
    """Represents the current authenticated user."""

    def __init__(
        self,
        user_id: int,
        email: str,
        roles: list[str]
    ):
        self.user_id = user_id
        self.email = email
        self.roles = roles

    def has_role(self, role: str) -> bool:
        """Check if user has the specified role."""
        return role in self.roles


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """Extract and validate the current user from JWT token."""
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = AuthService.decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return CurrentUser(
        user_id=int(payload.sub),
        email=payload.email,
        roles=payload.roles
    )
