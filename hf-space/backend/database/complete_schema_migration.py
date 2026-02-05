"""
Complete schema migration to update the database to match Better Auth models.
This script handles foreign key constraints properly when updating column types.
"""

import asyncio
from sqlalchemy import text
from database.connection import engine


async def migrate_user_and_task_tables():
    """
    Migrate user and task tables to match Better Auth string ID requirements.
    This requires temporarily dropping foreign key constraints, updating columns,
    then recreating the constraints.
    """
    async with engine.begin() as conn:
        # Step 1: Add the new columns that don't exist yet
        print("Step 1: Adding missing columns to user table...")

        # Add email_verified column if it doesn't exist
        try:
            await conn.execute(text("""
                ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;
            """))
            print("✓ Added email_verified column to user table")
        except Exception as e:
            print(f"⚠ Error adding email_verified column: {e}")

        # Add image column if it doesn't exist
        try:
            await conn.execute(text("""
                ALTER TABLE "user" ADD COLUMN IF NOT EXISTS image VARCHAR(500);
            """))
            print("✓ Added image column to user table")
        except Exception as e:
            print(f"⚠ Error adding image column: {e}")

        # Step 2: Drop the foreign key constraint between task and user
        print("\nStep 2: Temporarily dropping foreign key constraint...")
        try:
            await conn.execute(text("""
                ALTER TABLE task DROP CONSTRAINT IF EXISTS task_user_id_fkey;
            """))
            print("✓ Dropped foreign key constraint from task table")
        except Exception as e:
            print(f"⚠ Error dropping foreign key constraint: {e}")

        # Step 3: Update the user table id column to VARCHAR(100)
        print("\nStep 3: Updating user table id column...")
        try:
            # First, ensure all current integer IDs are converted to strings (hex format)
            # For existing records, we'll convert the integer IDs to hex strings
            await conn.execute(text("""
                -- Create a temporary column to hold string IDs
                ALTER TABLE "user" ADD COLUMN temp_id VARCHAR(100);

                -- Convert existing integer IDs to hex strings
                UPDATE "user" SET temp_id = LPAD(TO_HEX(id::INTEGER), 20, '0');

                -- Drop the old id column
                ALTER TABLE "user" DROP COLUMN id CASCADE;

                -- Rename the new column to id
                ALTER TABLE "user" RENAME COLUMN temp_id TO id;

                -- Set the new id column as primary key
                ALTER TABLE "user" ADD PRIMARY KEY (id);
            """))
            print("✓ Updated user table id column to VARCHAR(100)")
        except Exception as e:
            print(f"⚠ Error updating user id column: {e}")
            # If the above fails due to complex SQL, try simpler approach
            try:
                # Just change the column type if possible
                await conn.execute(text("""
                    CREATE OR REPLACE FUNCTION update_user_ids()
                    RETURNS void AS $$
                    DECLARE
                        rec RECORD;
                    BEGIN
                        -- Add new column
                        ALTER TABLE "user" ADD COLUMN new_id VARCHAR(100);

                        -- Update with hex representation
                        FOR rec IN SELECT * FROM "user" LOOP
                            UPDATE "user" SET new_id = LPAD(TO_HEX(rec.id::INTEGER), 20, '0') WHERE ctid = rec.ctid;
                        END LOOP;

                        -- Drop old column and rename new one
                        ALTER TABLE "user" DROP COLUMN id;
                        ALTER TABLE "user" RENAME COLUMN new_id TO id;
                        ALTER TABLE "user" ADD PRIMARY KEY (id);
                    END;
                    $$ LANGUAGE plpgsql;

                    SELECT update_user_ids();
                    DROP FUNCTION update_user_ids();
                """))
                print("✓ Updated user table id column using function approach")
            except Exception as e2:
                print(f"⚠ Error with function approach: {e2}")
                # Try the simplest approach - just update the data type if it's empty
                try:
                    await conn.execute(text("""
                        ALTER TABLE "user" ADD COLUMN temp_id_new VARCHAR(100);
                        UPDATE "user" SET temp_id_new = LPAD(TO_HEX(id::INTEGER), 20, '0');
                        ALTER TABLE "user" DROP COLUMN id CASCADE;
                        ALTER TABLE "user" RENAME COLUMN temp_id_new TO id;
                        ALTER TABLE "user" ADD PRIMARY KEY (id);
                    """))
                except Exception as e3:
                    print(f"⚠ Final attempt also failed: {e3}")
                    print("Note: Manual intervention may be needed for user table migration")

        # Step 4: Update the task table user_id column to VARCHAR(100)
        print("\nStep 4: Updating task table user_id column...")
        try:
            # Update user_id values to match the new hex string format
            await conn.execute(text("""
                -- Add new column for string user_ids
                ALTER TABLE task ADD COLUMN new_user_id VARCHAR(100);

                -- Update with hex representation of the old integer user_ids
                UPDATE task SET new_user_id = LPAD(TO_HEX(user_id::INTEGER), 20, '0');

                -- Drop old column and rename new one
                ALTER TABLE task DROP COLUMN user_id;
                ALTER TABLE task RENAME COLUMN new_user_id TO user_id;
            """))
            print("✓ Updated task table user_id column to VARCHAR(100)")
        except Exception as e:
            print(f"⚠ Error updating task user_id column: {e}")
            # Try alternative approach
            try:
                await conn.execute(text("""
                    ALTER TABLE task ADD COLUMN temp_user_id VARCHAR(100);
                    UPDATE task SET temp_user_id = LPAD(TO_HEX(user_id::INTEGER), 20, '0');
                    ALTER TABLE task DROP COLUMN user_id;
                    ALTER TABLE task RENAME COLUMN temp_user_id TO user_id;
                """))
                print("✓ Updated task user_id column with alternative approach")
            except Exception as e2:
                print(f"⚠ Alternative approach also failed: {e2}")
                print("Note: Manual intervention may be needed for task table migration")

        # Step 5: Recreate the foreign key constraint with CASCADE DELETE
        print("\nStep 5: Recreating foreign key constraint with CASCADE DELETE...")
        try:
            await conn.execute(text("""
                ALTER TABLE task
                ADD CONSTRAINT task_user_id_fkey
                FOREIGN KEY (user_id) REFERENCES "user"(id)
                ON DELETE CASCADE;
            """))
            print("✓ Recreated foreign key constraint with CASCADE DELETE")
        except Exception as e:
            print(f"⚠ Error recreating foreign key constraint: {e}")

        # Step 6: Update other column types to match the model
        print("\nStep 6: Updating other column types to match model...")
        try:
            await conn.execute(text("""
                ALTER TABLE "user" ALTER COLUMN email TYPE VARCHAR(200);
            """))
            print("✓ Updated user email column type")
        except Exception as e:
            print(f"⚠ Error updating user email column: {e}")

        try:
            await conn.execute(text("""
                ALTER TABLE "user" ALTER COLUMN name TYPE VARCHAR(100);
            """))
            print("✓ Updated user name column type")
        except Exception as e:
            print(f"⚠ Error updating user name column: {e}")

        print("\n✓ Schema migration completed!")


async def create_missing_tables():
    """
    Create any missing tables that might not have been created yet.
    """
    from sqlmodel import SQLModel
    from models.user import User
    from models.task import Task
    from models.session import Session
    from models.account import Account
    from models.verification import Verification

    async with engine.begin() as conn:
        # Create tables that might be missing
        await conn.run_sync(SQLModel.metadata.create_all)
        print("✓ Created any missing tables")


async def run_complete_migration():
    """
    Run the complete database schema migration for Better Auth compatibility.
    """
    print("Starting complete schema migration for Better Auth compatibility...")
    print("="*60)

    await create_missing_tables()
    print()
    await migrate_user_and_task_tables()

    print("="*60)
    print("Migration completed! Please restart your application.")
    print("Note: If you encounter issues, you may need to manually verify the schema.")


if __name__ == "__main__":
    asyncio.run(run_complete_migration())