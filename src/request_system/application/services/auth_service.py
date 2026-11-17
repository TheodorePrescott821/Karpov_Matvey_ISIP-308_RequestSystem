"""Authentication service for user login and password management."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from pydantic import BaseModel

from request_system.config import settings


class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: str  # user_id
    email: str
    roles: list[str]
    exp: datetime
    iat: datetime


class AuthService:
    """Handles authentication logic including password hashing and JWT token generation."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its bcrypt hash."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def create_token(
        user_id: int,
        email: str,
        roles: list[str],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT token with user data."""
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.jwt_expiration_minutes)

        now = datetime.now(timezone.utc)
        expire = now + expires_delta

        payload = {
            "sub": str(user_id),
            "email": email,
            "roles": roles,
            "exp": expire,
            "iat": now
        }

        encoded_jwt = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[TokenPayload]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm]
            )
            return TokenPayload(**payload)
        except JWTError:
            return None
