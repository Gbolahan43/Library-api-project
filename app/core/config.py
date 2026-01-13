from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Library API"
    
    # DATABASE
    DATABASE_URL: str = "sqlite:///./library.db"
    
    # FINES
    FINE_RATE_PER_DAY: float = 50.0
    DEFAULT_BORROWING_PERIOD: int = 14
    
    # ENVIRONMENT
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
