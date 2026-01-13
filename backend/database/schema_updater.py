"""
Schema updater for existing database tables.
This script adds missing columns to existing tables to match the current models.
"""

import asyncio
from sqlalchemy import text
from database.connection import engine


async def update_user_table_schema():
    """
    Add missing columns to the user table to match the current User model.
    """
    async with engine.begin() as conn:
        # Add email_verified column if it doesn't exist
        try:
            await conn.execute(text("""
                ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;
            """))
            print("Added email_verified column to user table if it didn't exist")
        except Exception as e:
            print(f"Error adding email_verified column: {e}")

        # Add image column if it doesn't exist
        try:
            await conn.execute(text("""
                ALTER TABLE "user" ADD COLUMN IF NOT EXISTS image VARCHAR(500);
            """))
            print("Added image column to user table if it didn't exist")
        except Exception as e:
            print(f"Error adding image column: {e}")

        # Update the id column to be VARCHAR instead of SERIAL if needed
        try:
            # Change id column type to VARCHAR(100) to match the model
            await conn.execute(text("""
                ALTER TABLE "user" ALTER COLUMN id TYPE VARCHAR(100);
            """))
            print("Updated user id column type to VARCHAR(100)")
        except Exception as e:
            print(f"Error updating id column type: {e}")

        # Ensure email column is VARCHAR(200) to match the model
        try:
            await conn.execute(text("""
                ALTER TABLE "user" ALTER COLUMN email TYPE VARCHAR(200);
            """))
            print("Updated user email column type to VARCHAR(200)")
        except Exception as e:
            print(f"Error updating email column type: {e}")

        # Ensure name column is VARCHAR(100) to match the model
        try:
            await conn.execute(text("""
                ALTER TABLE "user" ALTER COLUMN name TYPE VARCHAR(100);
            """))
            print("Updated user name column type to VARCHAR(100)")
        except Exception as e:
            print(f"Error updating name column type: {e}")


async def update_task_table_schema():
    """
    Update the task table to use string user_id for Better Auth compatibility.
    """
    async with engine.begin() as conn:
        # Update user_id column type to VARCHAR(100) to match Better Auth string IDs
        try:
            await conn.execute(text("""
                ALTER TABLE task ALTER COLUMN user_id TYPE VARCHAR(100);
            """))
            print("Updated task user_id column type to VARCHAR(100) for Better Auth compatibility")
        except Exception as e:
            print(f"Error updating task user_id column type: {e}")


async def update_schema():
    """
    Update the database schema to match current models.
    """
    print("Updating database schema to match current models...")

    await update_user_table_schema()
    await update_task_table_schema()

    print("Schema update completed!")


if __name__ == "__main__":
    asyncio.run(update_schema())