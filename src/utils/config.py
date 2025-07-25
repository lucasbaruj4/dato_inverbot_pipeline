"""
Configuration management for the Inverbot Data Pipeline.

This module handles all configuration settings using Pydantic for validation
and type safety.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

from pydantic import BaseSettings, Field, validator
from pydantic_settings import BaseSettings as PydanticBaseSettings


class Config(PydanticBaseSettings):
    """Configuration class for the Inverbot Data Pipeline."""
    
    # Database Configuration
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_api_key: str = Field(..., description="Supabase API key")
    pinecone_api_key: str = Field(..., description="Pinecone API key")
    pinecone_environment: str = Field(default="us-east-1", description="Pinecone environment")
    
    # Model Configuration (Colab via localtunnel)
    mistral_model_url: str = Field(..., description="Mistral model endpoint via localtunnel")
    embedding_model_url: str = Field(..., description="Embedding model endpoint via localtunnel")
    model_api_headers: Dict[str, str] = Field(
        default={"bypass-tunnel-reminder": "true", "Content-Type": "application/json"},
        description="Headers for localtunnel API calls"
    )
    
    # Application Configuration
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Data Processing Configuration
    max_retry_attempts: int = Field(default=3, description="Maximum retry attempts")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    batch_size: int = Field(default=100, description="Batch size for processing")
    chunk_size: int = Field(default=500, description="Text chunk size for embeddings")
    chunk_overlap: int = Field(default=50, description="Text chunk overlap")
    
    # File Storage
    download_dir: str = Field(default="./downloads", description="Download directory")
    temp_dir: str = Field(default="./temp", description="Temporary directory")
    cache_dir: str = Field(default="./cache", description="Cache directory")
    
    # Rate Limiting
    rate_limit_requests_per_minute: int = Field(default=60, description="Rate limit requests per minute")
    rate_limit_delay_seconds: int = Field(default=1, description="Rate limit delay in seconds")
    
    # Security
    encryption_key: Optional[str] = Field(default=None, description="Encryption key")
    jwt_secret: Optional[str] = Field(default=None, description="JWT secret")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    metrics_port: int = Field(default=8000, description="Metrics port")
    
    # Testing
    test_database_url: Optional[str] = Field(default=None, description="Test database URL")
    test_pinecone_index: Optional[str] = Field(default=None, description="Test Pinecone index")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @validator("model_api_headers", pre=True)
    def parse_model_api_headers(cls, v):
        """Parse model API headers from string if needed."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format for model_api_headers")
        return v
    
    @validator("download_dir", "temp_dir", "cache_dir")
    def create_directories(cls, v):
        """Create directories if they don't exist."""
        Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    def get_model_headers(self) -> Dict[str, str]:
        """Get headers for model API calls."""
        return self.model_api_headers.copy()
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app_env.lower() == "development"
    
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.app_env.lower() == "testing"


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config() -> Config:
    """Reload the configuration from environment variables."""
    global _config
    _config = Config()
    return _config


def validate_config() -> bool:
    """Validate the configuration and return True if valid."""
    try:
        config = get_config()
        # Additional validation logic can be added here
        return True
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        return False 