from datetime import datetime
from datetime import timezone
from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declarative_mixin,
    DeclarativeBase,
)
from sqlalchemy.ext.asyncio import AsyncAttrs


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata


@declarative_mixin
class PrimaryKeyMixin:
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )


@declarative_mixin
class DateTimeMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(tz=timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc),
    )


@declarative_mixin
class ActiveMixin:
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )


class BaseModel(PrimaryKeyMixin, DateTimeMixin, Base):
    __abstract__ = True
