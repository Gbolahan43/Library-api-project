from pydantic_settings import BaseSettings
from typing import Optional, List, Union
from pydantic import AnyHttpUrl, validator

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
    
    # CORS
    # Support comma-separated strings or list of origins
    BACKEND_CORS_ORIGINS: List[str] = ["*", "http://localhost:8000", "http://127.0.0.1:8000"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore" # Ignore extra fields in .env to prevent crashing

settings = Settings()
