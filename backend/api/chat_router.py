"""
Chat router for chatbot backend API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlmodel import Session
from typing import Dict, Any, Optional
from uuid import UUID
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
from agents.chat_agent import chat_agent
from mcp.tools import MCPTaskTools

# Create the router
chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.post("/{user_id}/conversation")
async def create_or_continue_conversation(
    user_id: str,
    message_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_chat_user),
    db: Session = Depends(get_db_session)
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

        # Validate and convert conversation_id if provided
        conversation_id = None
        if conversation_id_str:
            try:
                conversation_id = UUID(conversation_id_str)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation_id format"
                )

        # Get or create conversation
        if conversation_id:
            # Verify that the conversation belongs to the user
            conversation = db.get(Conversation, conversation_id)
            if not conversation or str(conversation.user_id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or access denied"
                )
        else:
            # Create a new conversation
            conversation = Conversation(
                user_id=UUID(user_id),
                metadata={}
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        # Create user message
        user_message_obj = Message(
            conversation_id=conversation.id,
            sender="user",
            content=user_message,
            timestamp=datetime.utcnow()
        )
        db.add(user_message_obj)
        db.commit()

        # Initialize the chat agent with database session
        await chat_agent.initialize_tools(db)

        # Prepare conversation context for the AI agent
        # For now, we'll use a simple approach - in a real implementation,
        # we'd fetch the recent conversation history
        conversation_context = []

        # Process the user message through the AI agent
        ai_response = await chat_agent.process_with_retry(
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
        db.commit()

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
        # Log the error (in a real implementation)
        print(f"Error in create_or_continue_conversation: {str(e)}")

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
    db: Session = Depends(get_db_session)
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
        # Validate conversation_id format
        try:
            conv_id = UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation_id format"
            )

        # Verify that the conversation belongs to the user
        conversation = db.get(Conversation, conv_id)
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

        messages = db.exec(messages_query).all()

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
        # Log the error (in a real implementation)
        print(f"Error in get_conversation_history: {str(e)}")

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
    db: Session = Depends(get_db_session)
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
        # Validate conversation_id format
        try:
            conv_id = UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation_id format"
            )

        # Verify that the conversation belongs to the user
        conversation = db.get(Conversation, conv_id)
        if not conversation or str(conversation.user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )

        # Delete the conversation (messages will be deleted due to CASCADE)
        db.delete(conversation)
        db.commit()

        return {
            "success": True,
            "message": "Conversation deleted successfully"
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error (in a real implementation)
        print(f"Error in delete_conversation: {str(e)}")

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
    db: Session = Depends(get_db_session)
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