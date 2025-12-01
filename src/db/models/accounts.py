from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import ActiveMixin, BaseModel


if TYPE_CHECKING:
    from db.models import User
    from db.models import UtilityProvider


class Account(ActiveMixin, BaseModel):
    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="accounts",
    )
    utility_provider_id: Mapped[int | None] = mapped_column(
        ForeignKey("utility_providers.id"),
        nullable=True,
    )
    utility_provider: Mapped["UtilityProvider"] = relationship(
        "UtilityProvider",
        back_populates="accounts",
    )
    number: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Account(id={self.id}, user_id={self.user_id}, utility_provider_id={self.utility_provider_id}, number={self.number})"
