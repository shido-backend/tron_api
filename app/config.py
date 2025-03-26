from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./tron_wallet.db"
    tron_network: str = "shasta"

    DEBUG: bool = True
    LOG_LEVEL: str = "CRITICAL" # DEBUG, INFO, WARNING, ERROR, CRITICAL
    EXTERNAL_LOGGING_ENABLED: bool = False
    ELASTICSEARCH_URL: Optional[str] = None
    SENTRY_DSN: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()