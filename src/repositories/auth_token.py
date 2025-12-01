from typing import Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.auth_tokens import AuthToken
from repositories.base import BaseRepository


class AuthTokenRepository(BaseRepository[AuthToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AuthToken)

    async def create_auth_token(
        self,
        user_id: int,
        access_token: str,
        expires_at: datetime,
    ) -> AuthToken:
        auth_token = AuthToken(
            user_id=user_id, access_token=access_token, expires_at=expires_at
        )
        self.session.add(auth_token)
        await self.session.commit()
        await self.session.refresh(auth_token)
        return auth_token

    async def get_by_user_id(self, user_id: int) -> Optional[AuthToken]:
        stmt = select(AuthToken).where(AuthToken.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_auth_token(
        self, user_id: int, access_token: str, expires_at: datetime
    ) -> Optional[AuthToken]:
        auth_token = await self.get_by_user_id(user_id)
        if not auth_token:
            return None

        auth_token.access_token = access_token
        auth_token.expires_at = expires_at

        await self.session.commit()
        await self.session.refresh(auth_token)
        return auth_token
