from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from loguru import logger

from core.settings.app import AppSettings

# Импортируем все модели для инициализации
import db.models  # noqa


class DatabaseManager:
    def __init__(self, settings: AppSettings):
        self.settings = settings
        self.engine: AsyncEngine | None = None
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def init_db(self) -> None:
        if self.engine:
            return

        self.engine = create_async_engine(
            self.settings.db.get_dsn(),
            poolclass=AsyncAdaptedQueuePool,
            pool_size=self.settings.db.pool_size,
            max_overflow=self.settings.db.max_overflow,
            pool_timeout=self.settings.db.pool_timeout,
            pool_recycle=self.settings.db.pool_recycle,
            pool_pre_ping=self.settings.db.pool_pre_ping,
            echo=self.settings.db.echo,
        )

        self.session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    async def close_db(self) -> None:
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.session = None

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if self.session is None:
            await self.init_db()

        if self.session is not None:
            async with self.session() as session:
                try:
                    yield session
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.close()

    async def health_check(self) -> bool:
        """Проверка возможности подключения к БД"""
        if self.engine is None:
            return False
        try:
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
