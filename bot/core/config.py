from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str | None = None

    class Config:
        env_file = '.env'

def load_config(path: str) -> Settings:
    conf = Settings()
    return conf

