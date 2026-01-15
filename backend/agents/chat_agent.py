"""
OpenAI Agent for chatbot backend.
Connects the OpenAI Agent to MCP tools for natural language processing.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from mcp.server import mcp_server
from mcp.config import config
from mcp.tools import MCPTaskTools
from database.session import get_db_session
from models.user import User
from models.conversation import Conversation
from models.message import Message
from sqlmodel import Session


class ChatAgent:
    """
    OpenAI Agent that processes natural language and connects to MCP tools.
    """

    def __init__(self):
        """Initialize the chat agent with OpenAI client and tools."""
        self.openai_client = AsyncOpenAI(api_key=config.openai_api_key)
        self.model = config.openai_model
        self.timeout = config.ai_operation_timeout

        # Initialize tools registry
        self.tools_registry = {}

    async def initialize_tools(self, db_session: Session):
        """Initialize the MCP tools for the agent."""
        # Create tools instance
        tools_instance = MCPTaskTools(db_session)

        # Register tools with the agent
        self.tools_registry = {
            "add_task": {
                "function": tools_instance.add_task,
                "description": "Add a new task for a user. Parameters: user_id, title, description (optional), priority (high/medium/low, default:medium), due_date (YYYY-MM-DD, optional)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "title": {"type": "string", "description": "The task title"},
                        "description": {"type": "string", "description": "The task description (optional)"},
                        "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "Task priority (default: medium)"},
                        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format (optional)"}
                    },
                    "required": ["user_id", "title"]
                }
            },
            "list_tasks": {
                "function": tools_instance.list_tasks,
                "description": "List tasks for a user. Parameters: user_id, status (all/pending/completed, default:all)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by status (default: all)"}
                    },
                    "required": ["user_id"]
                }
            },
            "complete_task": {
                "function": tools_instance.complete_task,
                "description": "Mark a task as completed. Parameters: user_id, task_id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID to complete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "delete_task": {
                "function": tools_instance.delete_task,
                "description": "Delete a task. Parameters: user_id, task_id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            },
            "update_task": {
                "function": tools_instance.update_task,
                "description": "Update a task. Parameters: user_id, task_id, and any of: title, description, priority, due_date, completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID to update"},
                        "title": {"type": "string", "description": "New title (optional)"},
                        "description": {"type": "string", "description": "New description (optional)"},
                        "priority": {"type": "string", "enum": ["high", "medium", "low"], "description": "New priority (optional)"},
                        "due_date": {"type": "string", "description": "New due date in YYYY-MM-DD format (optional)"},
                        "completed": {"type": "boolean", "description": "New completion status (optional)"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }

    async def process_natural_language(
        self,
        user_id: str,
        user_message: str,
        conversation_context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process natural language input and select appropriate MCP tool.

        Args:
            user_id: The ID of the user
            user_message: The natural language message from the user
            conversation_context: Previous conversation context (optional)

        Returns:
            Dict containing response and any actions taken
        """
        # Prepare the system message with tool information
        system_message = f"""
        You are a helpful assistant that helps users manage their tasks through natural language.
        You have access to several tools to perform task operations.
        Always respect the user's privacy and only operate on tasks that belong to the user.

        When a user wants to list tasks, first ask for clarification if they want all, pending, or completed tasks.

        When a user wants to update, complete, or delete a task, they may not know the exact task ID.
        In these cases, you should first list the user's tasks to identify the correct one before performing the operation.
        This is a two-step process:
        1. First, call the list_tasks tool to get the user's tasks
        2. Then, use the information from the list to call the appropriate tool with the correct task ID

        For example, if a user says "Complete the meeting task", you would:
        1. Call list_tasks to get all their tasks
        2. Identify which task matches "meeting" from the list
        3. Call complete_task with the correct task ID

        Be helpful and confirm actions when completing or deleting tasks.
        """

        # Prepare messages for the OpenAI API
        messages = [{"role": "system", "content": system_message}]

        # Add conversation context if provided
        if conversation_context:
            for msg in conversation_context:
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        # Prepare tools for the API call
        tools = []
        for tool_name, tool_info in self.tools_registry.items():
            tools.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"]
                }
            })

        try:
            # Call the OpenAI API with tools
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",  # Let the model decide whether to use tools
                timeout=self.timeout
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # If the model wants to call tools
            tool_results = []
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Validate that the tool exists
                    if function_name not in self.tools_registry:
                        raise ValueError(f"Unknown tool: {function_name}")

                    # Call the tool with the provided arguments
                    tool_func = self.tools_registry[function_name]["function"]

                    # Add user_id to function args if not already present
                    if "user_id" not in function_args:
                        function_args["user_id"] = user_id

                    # Execute the tool
                    tool_result = await tool_func(**function_args)

                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "result": tool_result
                    })

                # If there were tool calls, get the final response from the model
                # Add the tool results to the messages
                for tool_call in tool_calls:
                    messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call]
                    })

                for i, tool_result in enumerate(tool_results):
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(tool_result["result"]),
                        "tool_call_id": tool_calls[i].id
                    })

                # Get the final response from the model based on tool results
                final_response = await self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    timeout=self.timeout
                )

                final_content = final_response.choices[0].message.content
            else:
                # If no tools were called, use the model's direct response
                final_content = response_message.content

            # Format the response
            formatted_tool_calls = []
            for i, tool_call in enumerate(tool_calls or []):
                formatted_tool_calls.append({
                    "tool_name": tool_call.function.name,
                    "parameters": json.loads(tool_call.function.arguments),
                    "result": tool_results[i]["result"] if i < len(tool_results) else None
                })

            # Determine action type based on tool calls
            action_type = "message_processed"
            action_data = {}

            if tool_calls:
                # Map tool names to action types
                tool_to_action = {
                    "add_task": "task_created",
                    "complete_task": "task_updated",
                    "update_task": "task_updated",
                    "delete_task": "task_deleted",
                    "list_tasks": "task_listed"
                }

                # Use the first tool call for action type
                first_tool = tool_calls[0].function.name
                action_type = tool_to_action.get(first_tool, "operation_performed")

                # Extract relevant data from tool results
                if tool_results and "task" in tool_results[0]["result"]:
                    task_data = tool_results[0]["result"]["task"]
                    action_data = {
                        "task_id": task_data.get("id"),
                        "task_title": task_data.get("title"),
                        "success": tool_results[0]["result"].get("success", False)
                    }
                elif tool_results and "tasks" in tool_results[0]["result"]:
                    tasks_data = tool_results[0]["result"]["tasks"]
                    action_data = {
                        "task_count": len(tasks_data),
                        "success": tool_results[0]["result"].get("success", False)
                    }
                elif tool_results:
                    action_data = {
                        "success": tool_results[0]["result"].get("success", False),
                        "message": tool_results[0]["result"].get("message")
                    }

            return {
                "response": final_content or "Operation completed successfully.",
                "tool_calls": formatted_tool_calls,
                "action": {
                    "type": action_type,
                    "data": action_data
                }
            }

        except Exception as e:
            # Handle any errors in the AI processing
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}. Please try again.",
                "tool_calls": [],
                "action": {
                    "type": "error",
                    "data": {"error": str(e)}
                }
            }

    async def process_with_retry(
        self,
        user_id: str,
        user_message: str,
        conversation_context: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process natural language with retry logic.

        Args:
            user_id: The ID of the user
            user_message: The natural language message from the user
            conversation_context: Previous conversation context (optional)

        Returns:
            Dict containing response and any actions taken
        """
        import random

        for attempt in range(config.retry_attempts):
            try:
                result = await self.process_natural_language(user_id, user_message, conversation_context)
                return result
            except Exception as e:
                if attempt == config.retry_attempts - 1:
                    # Last attempt, return error response
                    return {
                        "response": "Sorry, I'm experiencing difficulties processing your request. Please try again later.",
                        "tool_calls": [],
                        "action": {
                            "type": "error",
                            "data": {"error": str(e)}
                        }
                    }

                # Wait before retry with exponential backoff
                delay = min(config.base_retry_delay * (2 ** attempt) + random.uniform(0, 1), config.max_retry_delay)
                await asyncio.sleep(delay)

        # This should not be reached, but included for completeness
        return {
            "response": "Processing failed after all retry attempts.",
            "tool_calls": [],
            "action": {
                "type": "error",
                "data": {"error": "Max retries exceeded"}
            }
        }


# Global chat agent instance
chat_agent = ChatAgent()


async def initialize_chat_agent():
    """Initialize the chat agent with tools."""
    # We need a database session to initialize tools
    # In a real implementation, this would be handled properly
    pass