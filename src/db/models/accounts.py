from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import ActiveMixin, BaseModel


if TYPE_CHECKING:
    from db.models import User
    from db.models import UtilityCompany


class Account(ActiveMixin, BaseModel):
    __tablename__ = "accounts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="accounts",
    )
    utility_company_id: Mapped[int] = mapped_column(
        ForeignKey("utility_companies.id"),
    )
    utility_company: Mapped["UtilityCompany"] = relationship(
        "UtilityCompany",
        back_populates="accounts",
    )
    number: Mapped[str] = mapped_column(String)
