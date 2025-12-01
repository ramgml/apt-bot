from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from repositories.base import BaseRepository

from db.models.accounts import Account

if TYPE_CHECKING:
    from db.models.users import User


class AccountRepository(BaseRepository[Account]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Account)

    async def get_by_user(self, user: "User") -> list[Account]:
        stmt = (
            select(Account)
            .where(Account.user_id == user.id)
            .options(selectinload(Account.utility_provider))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Account | None:
        stmt = (
            select(Account)
            .where(Account.id == id)
            .options(selectinload(Account.utility_provider))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Account]:
        stmt = select(Account).options(selectinload(Account.utility_provider))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **kwargs) -> Account:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        # Load relationships to avoid lazy loading issues
        stmt = (
            select(Account)
            .where(Account.id == obj.id)
            .options(selectinload(Account.utility_provider))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, obj_id: int) -> bool:
        obj = await self.get_by_id(obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def update(self, obj_id: int, **kwargs) -> Account | None:
        obj = await self.get_by_id(obj_id)
        if not obj:
            return None

        if email := kwargs.pop("email", None):
            obj.utility_provider.email = email

        for key, value in kwargs.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)

        # Load relationships to avoid lazy loading issues
        stmt = (
            select(Account)
            .where(Account.id == obj.id)
            .options(selectinload(Account.utility_provider))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
