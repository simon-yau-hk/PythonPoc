from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class MyConfig(BaseSettings):
    # App Configuration
    app_name: str = "Task Management API"
    debug: bool = False
    version: str = "1.0.0"
    
    # Database Configuration
    #Field(...): The ... means this field is required - no default value
    database_url: str = Field(..., description="Database connection URL")
    
    # Security
    secret_key: str = Field(..., description="Secret key for JWT tokens")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # External Services
    redis_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False

# Create a singleton instance
settings = MyConfig()