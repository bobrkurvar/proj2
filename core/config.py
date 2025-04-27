from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    BOT_TOKEN: str | None = None
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = '.env'

def load_config(path: str) -> Settings:
    conf = Settings(_env_file = path)
    return conf

