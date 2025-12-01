from enum import StrEnum
from functools import lru_cache
from typing import Type

# from pydantic import BaseModel

from core.settings.app import AppSettings
from core.settings.base import AppEnv, BaseAppSettings
from core.settings.envs.development import DevAppSettings
from core.settings.envs.production import ProdAppSettings
from core.settings.envs.test import TestAppSettings


# class GoogleOauthSettings(BaseModel):
#     auth_host: str = "http://localhost"
#     auth_port: int = 8000
#     google_client_id: str
#     google_client_secret: str

#     def google_client_creds(self) -> dict[str, Any]:
#         return {
#             "client_id": self.google_client_id,
#             "client_secret": self.google_client_secret,
#             "scopes": [
#                 "https://www.googleapis.com/auth/gmail.readonly",
#                 "https://www.googleapis.com/auth/gmail.send",
#                 "https://www.googleapis.com/auth/userinfo.email",
#                 "https://www.googleapis.com/auth/userinfo.profile",
#             ],
#             "redirect_uri": f"{self.auth_host}:{self.auth_port}/callback/gmail",
#         }


# class Settings(BaseSettings):
#     app_secret: SecretStr = SecretStr("secret")
#     api_token: str = "token"
#     bot_url: str = "https://t.me/bot"
#     log_level: str = "INFO"
#     db: PostgresSettings = PostgresSettings()

#     google: GoogleOAuthSettings = GoogleOAuthSettings()
#     # Настройки Gmail
#     gmail_max_retries: int = Field(
#         default=3,
#         description="Максимальное количество повторов для Gmail API",
#     )
#     gmail_timeout: int = Field(
#         default=30,
#         description="Timeout для Gmail API запросов",
#     )


environments: dict[AppEnv, Type[AppSettings]] = {
    AppEnv.dev: DevAppSettings,
    AppEnv.prod: ProdAppSettings,
    AppEnv.test: TestAppSettings,
}


@lru_cache
def get_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()


settings = get_settings()

DATABASE_URL = settings.db.get_dsn()


# Callbacks
class Callbacks(StrEnum):
    SEND = "send"
