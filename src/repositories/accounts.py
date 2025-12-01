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
        stmt = select(Account).where(Account.user_id == user.id).options(
            selectinload(Account.utility_company)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
