from sqlmodel import SQLModel
from database.connection import engine
from models.user import User
from models.task import Task
from models.session import Session
from models.account import Account
from models.verification import Verification

async def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This function should be called during application startup.
    """
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_db_and_tables())