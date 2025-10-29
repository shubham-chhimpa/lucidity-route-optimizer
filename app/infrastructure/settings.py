from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    average_speed_kmph: float = Field(20.0, env="AVERAGE_SPEED_KMPH")
    earth_radius_km: float = Field(6371.0, env="EARTH_RADIUS_KM")

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


