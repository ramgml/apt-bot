from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from core.config import settings
from db.manager import DatabaseManager

from api.routers import accounts, auth, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    db_manager = DatabaseManager(settings=settings)
    await db_manager.init_db()

    if await db_manager.health_check():
        logger.info("Database connection established successfully")
    else:
        logger.error("Failed to connect to database")

    yield

    await db_manager.close_db()
    logger.info("Application shutdown complete")


origins = [
    "http://localhost",
    "http://localhost:5050",
    "http://localhost:5173",
]


app = FastAPI(
    lifespan=lifespan,
    title="APT-BOT-API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)
