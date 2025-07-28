"""
Configuration management for the Inverbot Data Pipeline.

This module handles all configuration settings using Pydantic for validation
and type safety.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

from pydantic import Field, validator
from pydantic_settings import BaseSettings

logger = None  # Will be initialized later


class Config(BaseSettings):
    """Configuration class for the Inverbot Data Pipeline."""
    
    # Database Configuration
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_key: str = Field(..., description="Supabase API key")
    pinecone_api_key: str = Field(..., description="Pinecone API key")
    pinecone_environment: str = Field(default="us-east-1", description="Pinecone environment")
    
    # Google AI Model Configuration
    gemini_api_key: str = Field(..., description="Google Gemini API key")
    google_llm_model: str = Field(default="gemini-1.5-flash", description="Google LLM model name")
    google_embedding_model: str = Field(default="models/text-embedding-004", description="Google embedding model name")
    
    # Web Scraping APIs
    serper_api_key: str = Field(..., description="Serper API key for web search")
    firecrawl_api_key: str = Field(..., description="Firecrawl API key for web scraping")
    
    # Model Configuration for Context Efficiency
    max_input_tokens: int = Field(default=500, description="Maximum input tokens per request")
    max_output_tokens: int = Field(default=300, description="Maximum output tokens per request")
    temperature: float = Field(default=0.3, description="Model temperature for consistency")
    
    # Application Configuration
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Data Processing Configuration (Context-Efficient)
    max_retry_attempts: int = Field(default=3, description="Maximum retry attempts")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    batch_size: int = Field(default=2, description="Small batch size for testing")
    chunk_size: int = Field(default=300, description="Smaller text chunk size for embeddings")
    chunk_overlap: int = Field(default=30, description="Text chunk overlap")
    
    # File Storage
    download_dir: str = Field(default="./downloads", description="Download directory")
    temp_dir: str = Field(default="./temp", description="Temporary directory")
    cache_dir: str = Field(default="./cache", description="Cache directory")
    
    # Rate Limiting (Conservative for Cost Control)
    rate_limit_requests_per_minute: int = Field(default=20, description="Conservative rate limit")
    rate_limit_delay_seconds: int = Field(default=3, description="Rate limit delay in seconds")
    
    # Security
    encryption_key: Optional[str] = Field(default=None, description="Encryption key")
    jwt_secret: Optional[str] = Field(default=None, description="JWT secret")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    metrics_port: int = Field(default=8000, description="Metrics port")
    enable_token_monitoring: bool = Field(default=True, description="Enable token usage monitoring")
    token_monitoring_file: str = Field(default="./cache/token_usage.json", description="Token usage log file")
    
    # Testing
    test_database_url: Optional[str] = Field(default=None, description="Test database URL")
    test_pinecone_index: Optional[str] = Field(default=None, description="Test Pinecone index")
    
    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env.local
    
    @validator("download_dir", "temp_dir", "cache_dir")
    def create_directories(cls, v):
        """Create directories if they don't exist."""
        Path(v).mkdir(parents=True, exist_ok=True)
        return v
    
    def get_google_api_key(self) -> str:
        """Get Google AI API key."""
        return self.gemini_api_key
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration for Google AI."""
        return {
            "api_key": self.gemini_api_key,
            "llm_model": self.google_llm_model,
            "embedding_model": self.google_embedding_model,
            "max_input_tokens": self.max_input_tokens,
            "max_output_tokens": self.max_output_tokens,
            "temperature": self.temperature
        }
    
    @property
    def supabase_api_key(self) -> str:
        """Get Supabase API key (alias for supabase_key)."""
        return self.supabase_key


def get_config() -> Config:
    """Get the application configuration."""
    return Config()


def validate_config() -> bool:
    """Validate the configuration."""
    try:
        config = get_config()
        # Basic validation checks
        if not config.gemini_api_key:
            raise ValueError("Google Gemini API key is required")
        if not config.supabase_url or not config.supabase_key:
            raise ValueError("Supabase configuration is required")
        if not config.pinecone_api_key:
            raise ValueError("Pinecone configuration is required")
        return True
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        return False 