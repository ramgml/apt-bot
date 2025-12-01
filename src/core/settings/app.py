import logging
import sys
from typing import Any

from loguru import logger
from pydantic import Field, SecretStr

from core.logs import InterceptHandler
from core.settings.postgres import PostgresSettings
from core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Apt-bot"
    version: str = "0.0.0"

    app_secret: SecretStr = SecretStr("secret")
    api_token: str = "token"
    bot_url: str = "https://t.me/bot"
    log_level: str = "INFO"
    db: PostgresSettings = Field(default_factory=PostgresSettings)

    api_prefix: str = "/api"
    jwt_token_prefix: str = "Token"
    allowed_hosts: list[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: list[str] = [
        "uvicorn.asgi",
        "uvicorn.access",
        "api.main",
    ]

    class Config(BaseAppSettings.Config):
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
