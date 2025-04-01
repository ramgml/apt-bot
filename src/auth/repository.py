import logging
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User


log = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, tg_id: int) -> User | None:
        return await self.session.scalar(
            select(User).where(User.tg_id == tg_id)
        )

    async def create(
            self,
            *,
            tg_id: int,
            access_token: str,
            refresh_token: str,
            expires_at: datetime,
            email_from: str,
            email_to: str,
            account_number: str,
        ) -> User:
        user = User(
            tg_id=tg_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            email_from=email_from,
            email_to=email_to,
            account_number=account_number,
        )
        self.session.add(user)
        await self.session.commit()
        return user

    async def update(self, tg_id: int, **kwargs) -> User | None:
        user = await self.get(tg_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await self.session.commit()
        return user

    async def update_or_create(
            self,
            tg_id: int,
            *,
            access_token: str,
            refresh_token: str,
            expires_at: datetime,
            email_from: str,
            email_to: str | None = None,
            account_number: str | None= None,
        ) -> User:
        user = await self.get(tg_id)
        if user:
            user_data = {}
            if email_to:
                user_data['email_to'] = email_to
            if account_number:
                user_data['account_number'] = account_number

            user = await self.update(
                tg_id=tg_id,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at,
                email_from=email_from,
                **user_data
            )
            return False, user
        user = await self.create(
            tg_id=tg_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            email_from=email_from,
            email_to=email_to,
            account_number=account_number,
        )

        return True, user

    async def iterate_all(self, per_page: int = 1000) -> AsyncGenerator[User, None]:
        pointer = 0
        count = await self.session.scalar(select(User).count())
        for _ in range(count // per_page):
            page = await self.session.scalars(
                select(User).where(User.id > pointer).order_by(User.id).limit(per_page)
            )

            try:
                if user := page[-1]:
                    pointer = user.id
            except IndexError:
                break

            for user in page:
                yield user
