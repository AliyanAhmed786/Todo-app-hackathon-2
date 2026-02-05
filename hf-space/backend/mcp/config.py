"""Configuration for MCP Server."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class MCPConfig(BaseSettings):
    """Configuration settings for MCP server."""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")  # GPT-4 Turbo

    # Gemini Configuration - added as required by skill file
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")  # Required for Gemini API

    # Server Configuration
    server_host: str = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("MCP_SERVER_PORT", "8001"))

    # Retry Configuration
    retry_attempts: int = int(os.getenv("RETRY_ATTEMPTS", "3"))
    base_retry_delay: float = float(os.getenv("BASE_RETRY_DELAY", "1.0"))  # seconds
    max_retry_delay: float = float(os.getenv("MAX_RETRY_DELAY", "8.0"))   # seconds

    # Timeout Configuration
    ai_operation_timeout: int = int(os.getenv("AI_OPERATION_TIMEOUT", "10"))  # seconds
    db_query_timeout: int = int(os.getenv("DB_QUERY_TIMEOUT", "5"))          # seconds

    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "")

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


# Global configuration instance
config = MCPConfig()