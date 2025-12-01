from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import BaseModel


if TYPE_CHECKING:
    from db.models import User
    from db.models import UtilityProvider


class Reading(BaseModel):
    __tablename__ = "readings"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="readings",
    )
    utility_provider_id: Mapped[int] = mapped_column(
        ForeignKey("utility_providers.id"),
    )
    utility_provider: Mapped["UtilityProvider"] = relationship(
        "UtilityProvider",
        back_populates="readings",
    )
    value: Mapped[str] = mapped_column(
        String(255),
    )
