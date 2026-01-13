"""
Script to reset the database with the correct schema for Better Auth integration.
This will drop existing tables and recreate them with the correct schema.
"""

import asyncio
import os
from sqlalchemy import text
from database.connection import engine
from sqlmodel import SQLModel
from models.user import User
from models.task import Task
from models.session import Session
from models.account import Account
from models.verification import Verification


async def reset_database():
    """
    Reset the database by dropping all tables and recreating them with correct schema.
    """
    print("Resetting database with correct schema for Better Auth integration...")

    async with engine.begin() as conn:
        # Drop all tables
        print("Dropping all existing tables...")

        # Execute each command separately
        await conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        print("+ Dropped and recreated public schema")

    # Now recreate all tables with correct schema
    print("Recreating tables with correct schema...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        print("+ Created all tables with correct schema")

    print("\nDatabase reset complete!")
    print("Tables created:")
    print("- users: with string IDs and email_verified, image columns")
    print("- tasks: with string user_id foreign key and CASCADE DELETE")
    print("- sessions: for Better Auth database session validation")
    print("- accounts: for Better Auth account management")
    print("- verification: for Better Auth verification processes")
    print("\nYou can now start your application with the correct schema.")


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='sqlalchemy')

    print("WARNING: This will completely reset your database and delete all existing data!")
    response = input("Are you sure you want to continue? (yes/no): ")

    if response.lower() == 'yes':
        asyncio.run(reset_database())
    else:
        print("Database reset cancelled.")