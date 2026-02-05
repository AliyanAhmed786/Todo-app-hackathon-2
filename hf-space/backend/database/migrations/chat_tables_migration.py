"""
Database migration for chatbot tables: conversations and messages.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from database.connection import engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text


async def create_chat_tables():
    """Create conversations and messages tables."""
    async with engine.begin() as conn:
        # Create conversations table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS conversations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id VARCHAR(100) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            );
        """))

        # Create messages table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS messages (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                sender VARCHAR(20) NOT NULL CHECK (sender IN ('user', 'agent')),
                content TEXT NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            );
        """))

        # Create indexes
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);"))


async def create_chat_tables():
    """Create conversations and messages tables."""
    async with engine.begin() as conn:
        # Create conversations table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS conversations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id VARCHAR(100) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            );
        """))

        # Create messages table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS messages (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                sender VARCHAR(20) NOT NULL CHECK (sender IN ('user', 'agent')),
                content TEXT NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            );
        """))

        # Create indexes
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);"))


async def rollback_chat_tables():
    """Drop conversations and messages tables."""
    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS messages CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS conversations CASCADE;"))


import asyncio


if __name__ == "__main__":
    print("Creating chat tables...")
    asyncio.run(create_chat_tables())
    print("Chat tables created successfully!")