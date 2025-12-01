from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
)

from db.models.base import BaseModel
from db.models.accounts import Account
from db.models.readings import Reading


class UtilityProvider(BaseModel):
    __tablename__ = "utility_providers"

    name: Mapped[str] = mapped_column(
        String(255),
    )
    email: Mapped[str] = mapped_column(
        String(255),
    )
    accounts: Mapped[list["Account"]] = relationship(
        "Account",
        back_populates="utility_provider",
    )
    readings: Mapped[list["Reading"]] = relationship(
        "Reading",
        back_populates="utility_provider",
    )
