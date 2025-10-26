"""
Core Configuration Module
Centralized configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Optional
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    environment: str = "production"
    
    # Database
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    
    # Security
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # CORS - will be parsed from comma-separated string
    cors_origins: str = "http://localhost:3000"
    allowed_hosts: List[str] = ["*"]
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    # Agent Configuration
    max_conversation_history: int = 50
    learning_batch_size: int = 10
    model_update_interval: int = 3600
    
    # Manager Agent Communication
    manager_agent_url: Optional[str] = None
    
    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL is required")
        return v
    
    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret(cls, v):
        if not v:
            raise ValueError("JWT_SECRET_KEY is required")
        if len(v) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters")
        return v
    
    def get_cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string to list"""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(',')]
        return self.cors_origins
