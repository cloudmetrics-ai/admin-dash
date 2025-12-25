"""
Application Configuration
=========================

This module contains all configuration settings for the FastAPI application.
Settings are loaded from environment variables using Pydantic Settings.

Environment variables should be defined in a .env file in the backend directory.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import secrets


class Settings(BaseSettings):
    """
    Application Settings
    
    All settings are loaded from environment variables.
    Default values are provided for development, but should be overridden in production.
    
    Attributes:
        PROJECT_NAME: Name of the application
        VERSION: API version
        API_V1_STR: API version prefix for routes
        SECRET_KEY: Secret key for JWT token encoding (MUST be changed in production)
        ALGORITHM: Algorithm used for JWT encoding
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time in minutes
        DATABASE_URL: PostgreSQL connection string
        REDIS_URL: Redis connection string (optional)
        OPENAI_API_KEY: OpenAI API key for LLM features (optional)
        CORS_ORIGINS: List of allowed CORS origins
    """
    
    # ============================================================================
    # APPLICATION SETTINGS
    # ============================================================================
    
    PROJECT_NAME: str = "Admin Dashboard API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # ============================================================================
    # SECURITY SETTINGS
    # ============================================================================
    
    # Secret key for JWT encoding - MUST be changed in production!
    # Generate a secure key using: openssl rand -hex 32
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # JWT algorithm - HS256 is recommended for symmetric signing
    ALGORITHM: str = "HS256"
    
    # Token expiration time in minutes (30 minutes default)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Refresh token expiration in days (7 days default)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ============================================================================
    # DATABASE SETTINGS
    # ============================================================================
    
    # PostgreSQL connection string
    # Format: postgresql://username:password@host:port/database_name
    # Example: postgresql://admin:password123@localhost:5432/admin_dashboard
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/admin_dashboard"
    
    # Database pool settings for connection management
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # ============================================================================
    # REDIS SETTINGS (Optional - for caching and Celery)
    # ============================================================================
    
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"
    
    # ============================================================================
    # CELERY SETTINGS (Optional - for background tasks)
    # ============================================================================
    
    CELERY_BROKER_URL: Optional[str] = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: Optional[str] = "redis://localhost:6379/0"
    
    # ============================================================================
    # AI/LLM SETTINGS (Optional)
    # ============================================================================
    
    # OpenAI API key for GPT models
    OPENAI_API_KEY: Optional[str] = None
    
    # Default LLM model to use
    DEFAULT_LLM_MODEL: str = "gpt-4"
    
    # Maximum tokens for LLM responses
    MAX_LLM_TOKENS: int = 2000
    
    # ============================================================================
    # CORS SETTINGS
    # ============================================================================
    
    # List of allowed origins for CORS
    # In development, allow localhost. In production, specify your frontend domain.
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Next.js default dev server
        "http://localhost:8000",  # FastAPI dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # ============================================================================
    # FILE UPLOAD SETTINGS
    # ============================================================================
    
    # Maximum file upload size in bytes (10MB default)
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    
    # Allowed file extensions for uploads
    ALLOWED_EXTENSIONS: set[str] = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".txt", ".csv"}
    
    # Upload directory path
    UPLOAD_DIR: str = "./uploads"
    
    # ============================================================================
    # RATE LIMITING SETTINGS
    # ============================================================================
    
    # Maximum API requests per minute per user
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Maximum LLM requests per hour per user
    LLM_RATE_LIMIT_PER_HOUR: int = 100
    
    # ============================================================================
    # LOGGING SETTINGS
    # ============================================================================
    
    # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_LEVEL: str = "INFO"
    
    # ============================================================================
    # EMAIL/SMTP SETTINGS
    # ============================================================================
    
    # SMTP server configuration for sending emails
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: Optional[str] = None
    SMTP_FROM_NAME: Optional[str] = "Learn App"
    
    # ============================================================================
    # PYDANTIC SETTINGS CONFIGURATION
    # ============================================================================
    
    class Config:
        """
        Pydantic configuration
        
        - env_file: Load settings from .env file
        - case_sensitive: Environment variable names are case-sensitive
        """
        env_file = ".env"
        case_sensitive = True


# ============================================================================
# GLOBAL SETTINGS INSTANCE
# ============================================================================

# Create a single instance of settings to be imported throughout the application
# This ensures all modules use the same configuration
settings = Settings()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_database_url() -> str:
    """
    Get the database URL for SQLAlchemy
    
    Returns:
        str: PostgreSQL connection string
    """
    return settings.DATABASE_URL


def is_development() -> bool:
    """
    Check if the application is running in development mode
    
    Returns:
        bool: True if in development, False otherwise
    """
    return settings.LOG_LEVEL == "DEBUG"


def is_production() -> bool:
    """
    Check if the application is running in production mode
    
    Returns:
        bool: True if in production, False otherwise
    """
    return not is_development()
