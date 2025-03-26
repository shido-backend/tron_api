from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./tron_wallet.db"
    tron_network: str = "shasta"
    
    class Config:
        env_file = ".env"

settings = Settings()