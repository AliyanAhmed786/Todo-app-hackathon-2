"""
OpenAI Agent for chatbot backend.
Connects the OpenAI Agent to MCP tools for natural language processing.
"""

import asyncio
import json
import os
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
from sqlmodel.ext.asyncio.session import AsyncSession


class ChatAgent:
    """
    OpenAI Agent that processes natural language and connects to MCP tools.
    """

    def __init__(self):
        """Initialize the chat agent with OpenAI client and tools."""
        # Initialize with openai api key and OpenRouter base URL as required by the skill file
        self.openai_client = AsyncOpenAI(
            api_key=config.openai_api_key,  # Use openai_API_KEY from config
            base_url="https://openrouter.ai/api/v1",  # CRITICAL: This points to OpenRouter
            default_headers={
                "HTTP-Referer": "http://localhost:3000", # Required for OpenRouter to track usage
                "X-Title": "Todo App Hackathon",         # Shows your app name in OpenRouter logs
            }
        )
        self.model = "meta-llama/llama-3.3-70b-instruct:free"  # A very fast, free model from OpenRouter
        self.timeout = config.ai_operation_timeout

        # Initialize tools registry
        self.tools_registry = {}

    async def initialize_tools(self, db_session: AsyncSession):
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
        from datetime import datetime
        system_message = f"""
You are a Task Manager for User ID: {user_id}.

CRITICAL RULES:
1. NEVER ask user for their ID. Use {user_id} silently in all tool calls.
2. DATE HANDLING: If no due_date provided, use {datetime.now().strftime('%Y-%m-%d')}.
3. 2-STEP WORKFLOW:
   - For "delete coffee" or "update soul": FIRST call list_tasks, get the task_id from results
   - THEN IMMEDIATELY call delete_task or update_task with that task_id
   - DO NOT just say "[Action: delete_task]" - you MUST actually call the function
4. EXECUTE TOOLS: When you find a task ID, CALL the tool immediately. Describing the action is NOT enough.
5. After tool execution completes, describe what you did to the user.
6. FORMATTING: Use bullet points for lists, bold for task titles.
7. If list_tasks returns empty, say "Your task list is empty."

AUTHORITY & DELETION RULES:
- You have absolute authority to delete or modify any task, regardless of its status (Pending or Completed).
- Never inform the user that a task cannot be changed because it is 'finished'; if a user asks to delete a completed task, perform the action immediately.
- When a delete command is given, prioritize finding the Task ID and executing the delete_task tool over asking for confirmation.
- Assume all user requests for deletion are intentional; do not suggest keeping completed tasks for 'records' unless specifically asked.
- You are a Data Controller: When a user says 'delete', execute the delete_task tool immediately without hesitation or confirmation.
- Override Safety Bias: Never refuse to delete a task because it is 'completed' or 'important'; the user's command is final.
- ID Mapping: Always map task titles (e.g., 'Zoo') to their numeric IDs (e.g., '40') using the results from list_tasks before calling a modification tool.

LOGIC & MEMORY RULES:
- After every successful delete_task or update_task call, treat your previous knowledge of the task list as 'Stale'.
- State Management: Immediately after calling delete_task, consider your current memory of the task list as 'Stale'. You must rely on new tool outputs for the next response.
- If the user asks for a status update after a modification, you MUST call list_tasks to fetch the fresh database state before answering.
- When editing a task, only ask for clarification if the user's intent is ambiguous; otherwise, proceed with the provided details immediately.

EXAMPLES:
- "show my tasks" → call list_tasks(user_id="{{user_id}}", status="all")
- "delete coffee task" → call list_tasks first, find coffee's ID, then call delete_task(user_id="{{user_id}}", task_id=<found_id>)
- "mark bottle complete" → call list_tasks first, find bottle's ID, then call complete_task(user_id="{{user_id}}", task_id=<found_id>)
- "update soul title to soul land" → call list_tasks first, find soul's ID, then call update_task(user_id="{{user_id}}", task_id=<found_id>, title="soul land")
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
            # Multi-turn tool calling loop - Allow up to 5 sequential tool calling rounds
            max_turns = 5
            all_tool_calls = []  # Collect all tools used across all turns

            for turn in range(max_turns):
                # Call the OpenAI API with tools - with explicit error logging as required by skill file
                response = await self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",  # Let the model decide whether to use tools
                    timeout=self.timeout,
                    stream=False
                )

                # Process the response
                response_message = response.choices[0].message

                # Defensive Tool Parsing: Handle potential AttributeError on tool_calls
                tool_calls = getattr(response_message, 'tool_calls', None)

                # If the model wants to call tools
                tool_results = []
                if tool_calls:
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name

                        # Defensive parsing: Ensure arguments are not None or empty before parsing
                        arguments_str = getattr(tool_call.function, 'arguments', '{}').strip()
                        if not arguments_str or arguments_str == 'null':
                            arguments_str = '{}'

                        try:
                            function_args = json.loads(arguments_str)
                        except json.JSONDecodeError:
                            # Fallback to empty dict if JSON parsing fails
                            function_args = {}

                        # Validate that the tool exists
                        if function_name not in self.tools_registry:
                            raise ValueError(f"Unknown tool: {function_name}")

                        # Call the tool with the provided arguments
                        tool_func = self.tools_registry[function_name]["function"]

                        # Add user_id to function args if not already present
                        if "user_id" not in function_args:
                            function_args["user_id"] = user_id

                        # Execute the tool with due_date error handling
                        try:
                            tool_result = await tool_func(**function_args)
                        except Exception as e:
                            # Check if this is a due_date error and retry with default date
                            if "due_date" in str(e).lower():
                                # Add default due date and retry
                                function_args_with_default_date = function_args.copy()
                                from datetime import datetime
                                function_args_with_default_date["due_date"] = datetime.now().strftime('%Y-%m-%d')
                                try:
                                    tool_result = await tool_func(**function_args_with_default_date)
                                except Exception:
                                    # If retry also fails, re-raise the original error
                                    raise e
                            else:
                                # If not a due_date error, re-raise the original error
                                raise e

                        # Debug logging for tool result
                        print(f"🔥 TOOL RESULT: {function_name} returned: {tool_result}")

                        tool_results.append({
                            "tool_call_id": tool_call.id,
                            "result": tool_result
                        })

                    # Add the tool calls to the collection for the final response
                    for i, tool_call in enumerate(tool_calls):
                        # Defensive parsing: Safely extract arguments for formatting
                        arguments_str = getattr(tool_call.function, 'arguments', '{}').strip()
                        if not arguments_str or arguments_str == 'null':
                            arguments_str = '{}'

                        try:
                            parameters = json.loads(arguments_str)
                        except json.JSONDecodeError:
                            parameters = {}

                        all_tool_calls.append({
                            "tool_name": tool_call.function.name,
                            "parameters": parameters,
                            "result": tool_results[i]["result"] if i < len(tool_results) else None
                        })

                    # Add the tool results to the messages - keep adding to conversation history
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

                    # Continue to next turn - the loop will make another API call with updated messages
                    continue
                else:
                    # No tools called, break the loop and use the model's direct response
                    final_content = getattr(response_message, 'content', None)
                    break
            else:
                # If we've reached max turns, use the last response
                final_content = getattr(response.choices[0].message, 'content', None)

            # Final safety check: Ensure final_content is never None before returning the result
            if final_content is None:
                final_content = "I processed your request successfully."

            # Use the collected tool calls for the response
            formatted_tool_calls = all_tool_calls

            # Determine action type based on tool calls
            action_type = "message_processed"
            action_data = {}

            if all_tool_calls:
                # Map tool names to action types
                tool_to_action = {
                    "add_task": "task_created",
                    "complete_task": "task_updated",
                    "update_task": "task_updated",
                    "delete_task": "task_deleted",
                    "list_tasks": "task_listed"
                }

                # Use the first tool call for action type
                first_tool = all_tool_calls[0]["tool_name"]
                action_type = tool_to_action.get(first_tool, "operation_performed")

                # Extract relevant data from tool results
                if all_tool_calls and all_tool_calls[0]["result"]:
                    result = all_tool_calls[0]["result"]
                    if "task" in result:
                        task_data = result["task"]
                        action_data = {
                            "task_id": task_data.get("id"),
                            "task_title": task_data.get("title"),
                            "success": result.get("success", False)
                        }
                    elif "tasks" in result:
                        tasks_data = result["tasks"]
                        action_data = {
                            "task_count": len(tasks_data),
                            "success": result.get("success", False)
                        }
                    else:
                        action_data = {
                            "success": result.get("success", False),
                            "message": result.get("message")
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
            # Log failures with required format as specified in skill file
            print(f'❌ AI PROCESS CRASH: {e}')
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

async def get_chat_agent(db_session: AsyncSession):
    """
    Factory function to get a chat agent with initialized tools.
    This ensures the tools always have a fresh DB session.
    """
    agent = ChatAgent()
    await agent.initialize_tools(db_session)
    return agent