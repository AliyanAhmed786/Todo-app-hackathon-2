from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import Depends
from .connection import engine

from .connection import get_db_session_generator

# Export the session generator from connection.py to avoid duplicate session managers
get_db_session = get_db_session_generator