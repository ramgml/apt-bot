from pydantic_settings import BaseSettings
from enum import StrEnum
from pydantic import Field, SecretStr

from core.settings.google import GoogleOAuthSettings
from core.settings.postgres import PostgresSettings


class AppEnv(StrEnum):
    dev = "dev"
    prod = "prod"
    test = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnv = AppEnv.prod
    app_secret: SecretStr = SecretStr("secret")

    user_profile_host: str = "https://accounts.example.com"
    api_token: str = "token"
    bot_url: str = "https://t.me/bot"
    log_level: str = "INFO"
    db: PostgresSettings = PostgresSettings()

    google: GoogleOAuthSettings = GoogleOAuthSettings()
    # Настройки Gmail
    gmail_max_retries: int = Field(
        default=3,
        description="Максимальное количество повторов для Gmail API",
    )
    gmail_timeout: int = Field(
        default=30,
        description="Timeout для Gmail API запросов",
    )

    class Config:
        env_file = ".env"
        extra = "ignore"
