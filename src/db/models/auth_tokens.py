from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import ActiveMixin, BaseModel


class AuthToken(ActiveMixin, BaseModel):
    __tablename__ = 'auth_tokens'

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    access_token: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
