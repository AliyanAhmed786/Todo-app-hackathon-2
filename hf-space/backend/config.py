from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/todoapp")

    # JWT settings
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Debug settings
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"

    # Rate limiting settings
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # in seconds
    rate_limit_dashboard_requests: int = int(os.getenv("RATE_LIMIT_DASHBOARD_REQUESTS", "50"))  # Dashboard-specific rate limit

    # Properties to validate secrets in production
    @property
    def secret_key(self) -> str:
        key = os.getenv("SECRET_KEY")
        if not key and not self.debug:
            raise ValueError("SECRET_KEY environment variable is required in production (when DEBUG=False)")
        return key or "your-super-secret-key-here-keep-it-safe-and-long"  # Default for development only

    @property
    def better_auth_secret(self) -> str:
        secret = os.getenv("BETTER_AUTH_SECRET")
        if not secret and not self.debug:
            raise ValueError("BETTER_AUTH_SECRET environment variable is required in production (when DEBUG=False)")
        return secret or "your-better-auth-secret-key-here-keep-it-safe-and-long"  # Default for development only

# Create a single instance of settings
settings = Settings()

