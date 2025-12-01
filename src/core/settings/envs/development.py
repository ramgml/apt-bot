import logging

from core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev AptBot"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env"
