from typing import Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.refresh_tokens import RefreshToken
from repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RefreshToken)

    async def create_refresh_token(
        self, user_id: int, token: str, expires_at: datetime
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id, token=token, expires_at=expires_at
        )
        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)
        return refresh_token

    async def get_by_user_id(self, user_id: int) -> Optional[RefreshToken]:
        stmt = select(RefreshToken).where(RefreshToken.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_token(self, token: str) -> Optional[RefreshToken]:
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_refresh_token(
        self, user_id: int, token: str, expires_at: datetime
    ) -> Optional[RefreshToken]:
        refresh_token = await self.get_by_user_id(user_id)
        if not refresh_token:
            return None

        refresh_token.token = token
        refresh_token.expires_at = expires_at

        await self.session.commit()
        await self.session.refresh(refresh_token)
        return refresh_token

    async def delete_by_user_id(self, user_id: int) -> bool:
        refresh_token = await self.get_by_user_id(user_id)
        if not refresh_token:
            return False

        await self.session.delete(refresh_token)
        await self.session.commit()
        return True
