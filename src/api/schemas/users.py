# User Schemas
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """Base user schema."""

    telegram_id: int
    name: Optional[str] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""

    pass


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
