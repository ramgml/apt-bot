from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB__",  # все переменные будут начинаться с DB_
        case_sensitive=False,
        extra="forbid"
    )

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgre"
    postgres_password: str = "postgres"
    postgres_db: str = "postgres"
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600
    pool_pre_ping: bool = True
    echo: bool = False

    def get_dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                path=self.postgres_db,
            )
        )
