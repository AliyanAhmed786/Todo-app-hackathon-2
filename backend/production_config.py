"""
Production configuration for the Multi-User Todo Application API with Better Auth
"""
import os
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """
    Application settings for production environment with Better Auth database session validation
    """
    # App settings
    app_name: str = "Multi-User Todo Application API with Better Auth"
    app_version: str = "1.0.0"
    debug: bool = False

    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "30"))

    # Better Auth settings (database session validation)
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "43200"))  # 30 days for database session

    # CORS settings
    allowed_origins: List[str] = [
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "https://api.yourdomain.com",
        "http://localhost:3000",  # For local development with Next.js frontend
        "http://localhost:3001",  # Alternative dev port
        "http://localhost:8000"   # For local backend access
    ]

    # Rate limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hour in seconds

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "app.log")

    # Security
    trusted_hosts: List[str] = [
        "yourdomain.com",
        "*.yourdomain.com",
        "localhost",
        "127.0.0.1"
    ]

    # Better Auth HTTP-only cookie settings
    session_cookie_secure: bool = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"  # Set to true in production with HTTPS
    session_cookie_samesite: str = os.getenv("SESSION_COOKIE_SAMESITE", "lax")
    session_cookie_httponly: bool = True  # Always true for security

    class Config:
        env_file = ".env"


settings = Settings()