from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager
from config import settings
from typing import AsyncGenerator

# Create the async database engine with optimized settings for Neon PostgreSQL
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Set to True to see SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=280,     # Recycle connections after ~4.5 minutes (Neon timeout is 5 min)
    pool_size=20,         # Base pool size to handle concurrent connections
    max_overflow=10,      # Allow up to 10 additional connections during traffic spikes
    pool_timeout=30,      # Wait up to 30 seconds for a connection from the pool
    connect_args={
        "timeout": 10,    # Connection timeout in seconds
        "command_timeout": 30,  # Query execution timeout in seconds
        "server_settings": {
            "application_name": "TodoApp",
        }
    }
)

@asynccontextmanager
async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context manager for database sessions.
    Ensures the session is properly closed after use.
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_db_session_generator() -> AsyncGenerator[AsyncSession, None]:
    """
    Async generator function for FastAPI dependency injection.
    Properly handles session lifecycle to prevent connection leaks.
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()