import logging

from pydantic import SecretStr

from core.settings.app import AppSettings
from core.settings.postgres import PostgresSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Test AptBot"

    secret_key: SecretStr = SecretStr("test_secret")

    db: PostgresSettings = PostgresSettings(
       postgres_db="testing",
    )
    max_connection_count: int = 5
    min_connection_count: int = 5

    logging_level: int = logging.DEBUG
