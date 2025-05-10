from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    DATABASE_URL: PostgresDsn
    #ALGORITHM: str
    #SECRET_KEY: str
    #ACCESS_TOKEN_EXPIRE_MINUTES: int
    BOT_TOKEN: str

def load_config(path: Path) -> Settings:
   conf = Settings(_env_file=path)
   return conf