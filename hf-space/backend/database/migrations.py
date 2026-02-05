from sqlmodel import SQLModel
from database.connection import engine
from models.user import User
from models.task import Task
from models.session import Session
from models.account import Account
from models.verification import Verification
import asyncio
from sqlalchemy import text

async def create_db_and_tables():
    """
    Create database tables based on SQLModel models.
    This function should be called during application startup.
    """
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully!")


async def add_missing_columns():
    """
    Add missing columns to existing tables.
    This function adds the due_date column to the task table if it doesn't exist.
    """
    async with engine.begin() as conn:
        # Check if due_date column exists in task table
        result = await conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'task' AND column_name = 'due_date'
        """))

        if result.fetchone() is None:
            # Column doesn't exist, add it
            await conn.execute(text("ALTER TABLE task ADD COLUMN due_date DATE"))
            print("Added due_date column to task table successfully!")
        else:
            print("due_date column already exists in task table")


async def run_migrations():
    """
    Run all necessary migrations.
    """
    await create_db_and_tables()
    await add_missing_columns()


if __name__ == "__main__":
    asyncio.run(run_migrations())