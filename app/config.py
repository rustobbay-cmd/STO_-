from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str = Field(alias="BOT_TOKEN")
    admin_id: int = Field(alias="ADMIN_ID")
    timezone: str = Field(default="Europe/Moscow", alias="TIMEZONE")
    work_start_hour: int = Field(default=9, alias="WORK_START_HOUR")
    work_end_hour: int = Field(default=18, alias="WORK_END_HOUR")
    booking_days_ahead: int = Field(default=7, alias="BOOKING_DAYS_AHEAD")
    database_path: str = Field(default="sto.db", alias="DATABASE_PATH")

    @property
    def database_file(self) -> Path:
        return BASE_DIR / self.database_path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
