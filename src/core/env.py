from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'your project name'

    TELEGRAM_LOGGING_BOT_TOKEN: str
    TELEGRAM_LOGGING_CHAT_ID: int | str
    TELEGRAM_LOGGER_FORMAT: str = (
        f'{PROJECT_NAME}\n\n'
        '{level} {time:DD.MM.YYYY HH:mm:ss}\n'
        '{name}:{function}\n\n'
        '{message}'
    )

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=Path('../.env')
    )


env = Settings()
