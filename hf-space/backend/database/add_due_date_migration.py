"""
Database migration to add due_date column to tasks table.
Run this script to add the due_date field to existing task records.

Run from backend directory:
    cd backend
    python -m database.add_due_date_migration
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from database.connection import engine
from sqlmodel.ext.asyncio.session import AsyncSession

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def add_due_date_column():
    """
    Add due_date column to tasks table if it doesn't exist.
    Uses raw SQL to avoid model conflicts during migration.
    """
    async with AsyncSession(engine) as session:
        try:
            # Check if column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='task' AND column_name='due_date';
            """)
            
            result = await session.exec(check_query)
            exists = result.first()
            
            if not exists:
                # Add the column
                logger.info("Adding due_date column to task table...")
                alter_query = text("""
                    ALTER TABLE task 
                    ADD COLUMN due_date TIMESTAMP NULL;
                """)
                await session.exec(alter_query)
                await session.commit()
                logger.info("✅ Successfully added due_date column to task table")
            else:
                logger.info("ℹ️  due_date column already exists in task table")
                
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Error adding due_date column: {str(e)}")
            raise
        finally:
            await session.close()


async def main():
    """Main migration execution"""
    logger.info("Starting database migration: add due_date column")
    try:
        await add_due_date_column()
        logger.info("Migration completed successfully!")
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
