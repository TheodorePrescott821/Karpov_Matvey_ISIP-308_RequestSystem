"""Role-based access control decorators."""

from functools import wraps
from typing import Callable, Optional

from fastapi import HTTPException, status

from request_system.presentation.dependencies import CurrentUser


ROLES = {
    "applicant": "Заявитель",
    "operator": "Оператор",
    "executor": "Исполнитель",
    "reviewer": "Контролёр"
}


def require_role(*required_roles: str) -> Callable:
    """
    Decorator to check if the current user has one of the required roles.

    Usage:
        @app.post("/api/requests")
        @require_role("applicant", "operator")
        async def create_request(current_user: CurrentUser = Depends(get_current_user)):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user: Optional[CurrentUser] = kwargs.get("current_user")

            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            # Check if user has any of the required roles
            if not any(current_user.has_role(role) for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {', '.join(required_roles)}"
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def require_role_dependency(*required_roles: str) -> Callable:
    """
    Dependency version for use with Depends() in FastAPI.

    Usage:
        @app.post("/api/requests")
        async def create_request(
            current_user: CurrentUser = Depends(require_role_dependency("applicant"))
        ):
            ...
    """
    async def check_role(current_user: CurrentUser) -> CurrentUser:
        if not any(current_user.has_role(role) for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(required_roles)}"
            )
        return current_user

    return check_role
