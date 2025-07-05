"""
FastMCP 2.0 Client Demo with error handling, logging, and type hints.
"""

import asyncio
import logging
from typing import Any, Dict

from fastmcp import Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("MathMCPClient")

async def call_tool(tool_name: str, params: Dict[str, Any]) -> Any:
    """
    Call a tool on the MCP Server asynchronously.

    Args:
        tool_name (str): Name of the tool to call.
        params (dict): Parameters to pass to the tool.

    Returns:
        Any: Result returned from the tool (CallToolResult).

    Raises:
        Exception: If the call fails.
    """
    url = "http://127.0.0.1:8080/mcp"
    async with Client(url) as client:
        logger.info(f"Calling tool '{tool_name}' with params {params!r}")
        try:
            result = await client.call_tool(tool_name, params)
            logger.info(f"Received result: {result!r}")
            return result
        except Exception as e:
            logger.error(f"Error calling tool '{tool_name}': {e}")
            raise

async def main() -> None:
    """
    Run demo calls to the MCP server, showing both success and error handling.
    """
    try:
        # Successful add operation.
        add_result = await call_tool("add", {"a": 10, "b": 5})
        print(f"add(10, 5) = {add_result.data}")

        # Successful subtract operation,
        subtract_result = await call_tool("subtract", {"a": 20, "b": 7})
        print(f"subtract(20, 7) = {subtract_result.data}")

        # Error handling: invalid parameter operation.
        try:
            await call_tool("add", {"a": "foo", "b": 5})
        except Exception as e:
            logger.error(f"Caught error calling add with invalid params: {e}")

    except Exception as e:
        logger.error(f"Client error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
