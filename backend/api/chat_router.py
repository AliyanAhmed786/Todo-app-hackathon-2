"""
Chat router for chatbot backend API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict, Any, Optional
import uuid
import json
from datetime import datetime

from models.conversation import Conversation
from models.message import Message, MessageCreate
from models.user import User
from dependencies.chat_auth import get_current_chat_user
from database.session import get_db_session
from exceptions.chat_exceptions import (
    create_invalid_token_http_exception,
    create_user_id_mismatch_http_exception,
    create_database_operation_http_exception
)
from agents.chat_agent import get_chat_agent
from mcp.tools import MCPTaskTools

# Create the router
chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("/{user_id}/conversation")
async def create_or_continue_conversation(
    user_id: str,
    message_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_chat_user),
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Create a new conversation or continue an existing one.

    Args:
        user_id: The ID of the user (from path)
        message_data: Contains 'message' and optional 'conversation_id'
        background_tasks: FastAPI background tasks
        current_user: Authenticated user
        db: Database session

    Returns:
        Dict containing response, conversation_id, and any actions taken
    """
    try:
        # Extract message and conversation_id from request
        user_message = message_data.get("message", "").strip()
        conversation_id_str = message_data.get("conversation_id")

        if not user_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is required"
            )

        # Validate conversation_id if provided - but don't convert to UUID as per ID Type Safety Rule
        conversation_id = None
        if conversation_id_str:
            # Just assign the string value directly - Better Auth IDs are hex strings
            conversation_id = conversation_id_str

        # Get or create conversation
        if conversation_id:
            # Verify that the conversation belongs to the user
            conversation = await db.get(Conversation, conversation_id)
            if not conversation or str(conversation.user_id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or access denied"
                )
        else:
            # Create a new conversation - using raw user_id string as per ID Type Safety Rule
            conversation = Conversation(
                user_id=user_id,
                meta_data="{}"  # Use meta_data to match the model field name
            )
            print(f'DEBUG: Saving data for user {user_id}')
            db.add(conversation)
            print(f'DEBUG: Added conversation for user {user_id}')
            await db.commit()
            print(f'DEBUG: Committed conversation for user {user_id}')
            await db.refresh(conversation)
            print(f'DEBUG: Refreshed conversation for user {user_id}')

        # Create user message
        user_message_obj = Message(
            conversation_id=conversation.id,
            sender="user",
            content=user_message,
            timestamp=datetime.utcnow()
        )
        db.add(user_message_obj)
        print(f'DEBUG: Added user message for user {user_id}')
        await db.commit()
        print(f'DEBUG: Committed user message for user {user_id}')

        # Initialize the chat agent with database session using factory function
        agent = await get_chat_agent(db)  # New instance per request

        # Prepare conversation context for the AI agent
        # For now, we'll use a simple approach - in a real implementation,
        # we'd fetch the recent conversation history
        conversation_context = []

        # Process the user message through the AI agent
        ai_response = await agent.process_with_retry(
            user_id=user_id,
            user_message=user_message,
            conversation_context=conversation_context
        )

        # Create agent response message
        agent_message_obj = Message(
            conversation_id=conversation.id,
            sender="agent",
            content=ai_response.get("response", "I processed your request."),
            timestamp=datetime.utcnow()
        )
        db.add(agent_message_obj)
        print(f'DEBUG: Added agent message for user {user_id}')
        await db.commit()
        print(f'DEBUG: Committed agent message for user {user_id}')

        # Prepare the response
        response = {
            "response": ai_response.get("response", "I processed your request."),
            "conversation_id": str(conversation.id),
            "tool_calls": ai_response.get("tool_calls", []),
            "action": ai_response.get("action", {
                "type": "message_processed",
                "data": {
                    "user_message": user_message,
                    "conversation_id": str(conversation.id)
                }
            })
        }

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Explicit Exception Logging: Print specific error as required by skill file
        print(f"❌ BACKEND CRASH: {str(e)}")

        # Raise a generic error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred processing your request"
        )


@chat_router.get("/{user_id}/conversation/{conversation_id}")
async def get_conversation_history(
    user_id: str,
    conversation_id: str,
    current_user: User = Depends(get_current_chat_user),
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Get the history of a specific conversation.

    Args:
        user_id: The ID of the user (from path)
        conversation_id: The ID of the conversation (from path)
        current_user: Authenticated user
        db: Database session

    Returns:
        Dict containing conversation history
    """
    try:
        # Use conversation_id as a raw string - Better Auth IDs are hex strings that fail UUID validation
        conv_id = conversation_id

        # Verify that the conversation belongs to the user
        conversation = await db.get(Conversation, conv_id)
        if not conversation or str(conversation.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )

        # Get all messages in the conversation
        from sqlmodel import select
        messages_query = select(Message).where(
            Message.conversation_id == conv_id
        ).order_by(Message.timestamp)

        result = await db.exec(messages_query)
        messages = result.all()

        # Format the response
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "id": str(msg.id),
                "sender": msg.sender,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata
            })

        return {
            "conversation_id": str(conversation.id),
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "messages": formatted_messages
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Explicit Exception Logging: Print specific error as required by skill file
        print(f"❌ BACKEND CRASH: {str(e)}")

        # Raise a generic error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred retrieving conversation history"
        )


@chat_router.delete("/{user_id}/conversation/{conversation_id}")
async def delete_conversation(
    user_id: str,
    conversation_id: str,
    current_user: User = Depends(get_current_chat_user),
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Delete a specific conversation.

    Args:
        user_id: The ID of the user (from path)
        conversation_id: The ID of the conversation to delete (from path)
        current_user: Authenticated user
        db: Database session

    Returns:
        Dict confirming deletion
    """
    try:
        # Use conversation_id as a raw string - Better Auth IDs are hex strings that fail UUID validation
        conv_id = conversation_id

        # Verify that the conversation belongs to the user
        conversation = await db.get(Conversation, conv_id)
        if not conversation or str(conversation.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )

        # Delete the conversation (messages will be deleted due to CASCADE)
        db.delete(conversation)
        await db.commit()

        return {
            "success": True,
            "message": "Conversation deleted successfully"
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Explicit Exception Logging: Print specific error as required by skill file
        print(f"❌ BACKEND CRASH: {str(e)}")

        # Raise a generic error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred deleting the conversation"
        )


# Backward compatibility with the original endpoint structure
@chat_router.post("/{user_id}")
async def process_chat_message(
    user_id: str,
    message_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_chat_user),
    db: AsyncSession = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Process a chat message (backward compatible with original design).

    Args:
        user_id: The ID of the user (from path)
        message_data: Contains 'message' and optional 'conversation_id'
        background_tasks: FastAPI background tasks
        current_user: Authenticated user
        db: Database session

    Returns:
        Dict containing response and any actions taken
    """
    # This is just a wrapper to the main endpoint for backward compatibility
    return await create_or_continue_conversation(user_id, message_data, background_tasks, current_user, db)