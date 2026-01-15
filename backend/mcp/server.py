"""
MCP Server initialization for chatbot backend.
"""

import asyncio
import uvicorn
from typing import Dict, Any, Callable
from mcp.config import config
from mcp.tools import create_mcp_tools
from database.session import get_db_session


class MCPServer:
    """
    MCP Server that hosts the tools for the AI agent.
    """

    def __init__(self):
        """Initialize the MCP server."""
        self.tools = {}
        self.db_session = None

    async def initialize_tools(self):
        """Initialize the MCP tools with database access."""
        try:
            # Create database session
            self.db_session = next(get_db_session())

            # Create and register tools
            tools_instance = create_mcp_tools(self.db_session)

            # Register all tools
            self.tools = {
                "add_task": tools_instance.add_task,
                "list_tasks": tools_instance.list_tasks,
                "complete_task": tools_instance.complete_task,
                "delete_task": tools_instance.delete_task,
                "update_task": tools_instance.update_task
            }

            print("MCP tools initialized successfully")
        except Exception as e:
            print(f"Error initializing MCP tools: {e}")
            raise

    def get_tool(self, tool_name: str) -> Callable:
        """
        Get a tool by name.

        Args:
            tool_name: Name of the tool to retrieve

        Returns:
            Callable tool function
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        return self.tools[tool_name]

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool with the provided arguments.

        Args:
            tool_name: Name of the tool to execute
            **kwargs: Arguments to pass to the tool

        Returns:
            Result of the tool execution
        """
        tool = self.get_tool(tool_name)

        # For async tools, we need to handle them specially
        if asyncio.iscoroutinefunction(tool):
            # In a synchronous context, we'd need to run this in an event loop
            # For now, returning a placeholder - in practice, you'd need to handle async properly
            import inspect
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(tool(**kwargs))
                return result
            finally:
                loop.close()
        else:
            return tool(**kwargs)

    def close(self):
        """Close the database session."""
        if self.db_session:
            self.db_session.close()


# Global server instance
mcp_server = MCPServer()


async def startup_event():
    """Initialize the MCP server on startup."""
    await mcp_server.initialize_tools()


def shutdown_event():
    """Clean up the MCP server on shutdown."""
    mcp_server.close()


# Example of how to run the server (would be in a separate main.py or called from CLI)
def run_server():
    """Run the MCP server."""
    print(f"Starting MCP server on {config.server_host}:{config.server_port}")

    # In a real implementation, this would set up the actual server
    # For now, we're just showing the structure
    print("MCP Server initialized with tools:")
    for tool_name in mcp_server.tools.keys():
        print(f"  - {tool_name}")


if __name__ == "__main__":
    run_server()