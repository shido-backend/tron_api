from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    #API
    database_url: str = "sqlite:///./tron_wallet.db"
    tron_network: str = "shasta"

    # LOGGING
    DEBUG: bool = True
    LOG_LEVEL: str = "CRITICAL" # DEBUG, INFO, WARNING, ERROR, CRITICAL
    EXTERNAL_LOGGING_ENABLED: bool = False
    ELASTICSEARCH_URL: Optional[str] = None
    SENTRY_DSN: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    # CACHE
    CACHE_ENABLED: bool = True
    DEFAULT_CACHE_TTL: int = 300  # 5 минут
    CACHE_MAX_SIZE: int = 1000
    
    class Config:
        env_file = ".env"

settings = Settings()