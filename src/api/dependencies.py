
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.config import settings
from db.manager import DatabaseManager


# Dependency to get database session
async def get_db_session():
    db_manager = DatabaseManager(settings=settings)
    async for session in db_manager.get_session():
        yield session

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
