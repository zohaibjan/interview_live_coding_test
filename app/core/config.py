from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "sqlite:///./coding_test.db"
    redis_url: str = "redis://localhost:6379"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Code execution settings
    max_execution_time: int = 30  # seconds
    max_memory_limit: int = 128  # MB
    
    class Config:
        env_file = ".env"

settings = Settings()