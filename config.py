"""
Core Configuration Module
Centralized configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, Field
from typing import List, Optional, Union
import os
from pathlib import Path


class ProjectAgentSettings(BaseSettings):
    """
    Project Agent Configuration Settings
    All settings loaded from environment variables or .env file
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ============================================================================
    # SERVER CONFIGURATION
    # ============================================================================
    host: str = Field(default="0.0.0.0", env="PROJECT_AGENT_HOST")
    port: int = Field(default=8001, env="PROJECT_AGENT_PORT")
    environment: str = Field(default="production", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    worker_count: int = Field(default=4, env="WORKER_COUNT")
    
    # ============================================================================
    # DATABASE CONFIGURATION
    # ============================================================================
    database_url: str = Field(..., env="DATABASE_URL")
    database_pool_size: int = Field(default=20, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # ============================================================================
    # REDIS CONFIGURATION
    # ============================================================================
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_max_connections: int = Field(default=50, env="REDIS_MAX_CONNECTIONS")
    
    # ============================================================================
    # KAFKA CONFIGURATION
    # ============================================================================
    kafka_bootstrap_servers: Union[str, List[str]] = Field(
        default="localhost:9092",
        env="KAFKA_BOOTSTRAP_SERVERS"
    )
    kafka_topic_prefix: str = Field(default="project_agent", env="KAFKA_TOPIC_PREFIX")
    
    # ============================================================================
    # SECURITY CONFIGURATION
    # ============================================================================
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="RS256", env="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(default=60, env="JWT_EXPIRE_MINUTES")
    jwt_public_key_path: Optional[str] = Field(default=None, env="JWT_PUBLIC_KEY_PATH")
    jwt_private_key_path: Optional[str] = Field(default=None, env="JWT_PRIVATE_KEY_PATH")
    
    cors_origins: Union[str, List[str]] = Field(
        default="http://localhost:3000",
        env="CORS_ORIGINS"
    )
    trusted_hosts: Union[str, List[str]] = Field(
        default="localhost,127.0.0.1",
        env="TRUSTED_HOSTS"
    )
    
    rate_limit_enabled: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    rate_limit_requests_per_minute: int = Field(
        default=100,
        env="RATE_LIMIT_REQUESTS_PER_MINUTE"
    )
    
    # ============================================================================
    # QUALITY VERIFICATION
    # ============================================================================
    quality_threshold: float = Field(default=85.0, env="QUALITY_THRESHOLD")
    code_coverage_min: float = Field(default=80.0, env="CODE_COVERAGE_MIN")
    security_scan_enabled: bool = Field(default=True, env="SECURITY_SCAN_ENABLED")
    performance_benchmark_enabled: bool = Field(
        default=True,
        env="PERFORMANCE_BENCHMARK_ENABLED"
    )
    
    quality_code_weight: float = Field(default=0.35, env="QUALITY_CODE_WEIGHT")
    quality_security_weight: float = Field(default=0.30, env="QUALITY_SECURITY_WEIGHT")
    quality_performance_weight: float = Field(default=0.20, env="QUALITY_PERFORMANCE_WEIGHT")
    quality_documentation_weight: float = Field(
        default=0.15,
        env="QUALITY_DOCUMENTATION_WEIGHT"
    )
    
    # ============================================================================
    # FILE STORAGE
    # ============================================================================
    storage_backend: str = Field(default="local", env="STORAGE_BACKEND")
    storage_path: str = Field(default="./uploads", env="STORAGE_PATH")
    max_upload_size_mb: int = Field(default=100, env="MAX_UPLOAD_SIZE_MB")
    file_versioning_enabled: bool = Field(default=True, env="FILE_VERSIONING_ENABLED")
    
    # AWS S3
    aws_access_key_id: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    aws_region: Optional[str] = Field(default="us-east-1", env="AWS_REGION")
    s3_bucket: Optional[str] = Field(default=None, env="S3_BUCKET")
    
    # ============================================================================
    # AGENT REGISTRY
    # ============================================================================
    manager_agent_url: str = Field(
        default="http://manager-agent:8000",
        env="MANAGER_AGENT_URL"
    )
    coding_agent_url: str = Field(
        default="http://coding-agent:8010",
        env="CODING_AGENT_URL"
    )
    examination_agent_url: str = Field(
        default="http://examination-agent:8030",
        env="EXAMINATION_AGENT_URL"
    )
    enhancement_agent_url: str = Field(
        default="http://enhancement-agent:8020",
        env="ENHANCEMENT_AGENT_URL"
    )
    
    agent_request_timeout: int = Field(default=30, env="AGENT_REQUEST_TIMEOUT")
    agent_max_retries: int = Field(default=3, env="AGENT_MAX_RETRIES")
    
    # ============================================================================
    # MONITORING
    # ============================================================================
    prometheus_enabled: bool = Field(default=True, env="PROMETHEUS_ENABLED")
    prometheus_port: int = Field(default=9090, env="PROMETHEUS_PORT")
    
    jaeger_enabled: bool = Field(default=True, env="JAEGER_ENABLED")
    jaeger_agent_host: str = Field(default="localhost", env="JAEGER_AGENT_HOST")
    jaeger_agent_port: int = Field(default=6831, env="JAEGER_AGENT_PORT")
    
    log_format: str = Field(default="json", env="LOG_FORMAT")
    log_file: str = Field(default="./logs/project_agent.log", env="LOG_FILE")
    
    # ============================================================================
    # FEATURE FLAGS
    # ============================================================================
    enable_chat_interface: bool = Field(default=True, env="ENABLE_CHAT_INTERFACE")
    enable_file_versioning: bool = Field(default=True, env="ENABLE_FILE_VERSIONING")
    enable_auto_integration: bool = Field(default=True, env="ENABLE_AUTO_INTEGRATION")
    enable_rollback: bool = Field(default=True, env="ENABLE_ROLLBACK")
    
    # ============================================================================
    # VALIDATORS
    # ============================================================================
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v) -> List[str]:
        """Parse CORS origins from string or list"""
        if v is None or v == '':
            return ["http://localhost:3000"]
        if isinstance(v, str):
            # Handle comma-separated values
            origins = [s.strip() for s in v.split(',') if s.strip()]
            return origins if origins else ["http://localhost:3000"]
        if isinstance(v, list):
            return v
        return ["http://localhost:3000"]
    
    @field_validator('kafka_bootstrap_servers', mode='before')
    @classmethod
    def parse_kafka_servers(cls, v) -> List[str]:
        """Parse Kafka servers from string or list"""
        if v is None or v == '':
            return ["localhost:9092"]
        if isinstance(v, str):
            servers = [s.strip() for s in v.split(',') if s.strip()]
            return servers if servers else ["localhost:9092"]
        if isinstance(v, list):
            return v
        return ["localhost:9092"]
    
    @field_validator('trusted_hosts', mode='before')
    @classmethod
    def parse_trusted_hosts(cls, v) -> List[str]:
        """Parse trusted hosts from string or list"""
        if v is None or v == '':
            return ["localhost", "127.0.0.1"]
        if isinstance(v, str):
            hosts = [s.strip() for s in v.split(',') if s.strip()]
            return hosts if hosts else ["localhost", "127.0.0.1"]
        if isinstance(v, list):
            return v
        return ["localhost", "127.0.0.1"]
    
    @field_validator('storage_path')
    @classmethod
    def ensure_storage_path_exists(cls, v):
        """Create storage path if it doesn't exist"""
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return str(path.absolute())
    
    @field_validator('log_file')
    @classmethod
    def ensure_log_directory_exists(cls, v):
        """Create log directory if it doesn't exist"""
        path = Path(v).parent
        path.mkdir(parents=True, exist_ok=True)
        return v
    
    def get_agent_urls(self) -> dict:
        """Get all configured agent URLs"""
        return {
            "manager": self.manager_agent_url,
            "coding": self.coding_agent_url,
            "examination": self.examination_agent_url,
            "enhancement": self.enhancement_agent_url,
        }
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"


# Backwards compatibility alias
Settings = ProjectAgentSettings

# Global settings instance
settings = ProjectAgentSettings()
