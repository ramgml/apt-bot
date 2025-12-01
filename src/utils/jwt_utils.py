"""JWT utility functions for APT Bot."""

import jwt
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

from core.config import settings


def generate_jwt_token(telegram_user_id: int, email: str) -> str:
    """
    Generate JWT token for user.

    Args:
        user_id: User ID
        email: User email

    Returns:
        JWT token string
    """
    payload = {
        "user_id": telegram_user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(
        payload, settings.app_secret.get_secret_value(), algorithm="HS256"
    )


def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token, settings.app_secret.get_secret_value(), algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
