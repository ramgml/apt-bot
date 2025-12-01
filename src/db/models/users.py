from __future__ import annotations

from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import BaseModel, ActiveMixin
from db.models.accounts import Account
from db.models.readings import Reading


class User(ActiveMixin, BaseModel):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )
    accounts: Mapped[List["Account"]] = relationship(
        "Account",
        back_populates="user",
    )
    readings: Mapped[List["Reading"]] = relationship(
        "Reading",
        back_populates="user",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"
