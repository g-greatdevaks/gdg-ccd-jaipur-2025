"""
Math MCP Server using FastMCP 2.0

This server exposes arithmetic tools and a number-in-words explainer
using the FastMCP 2.0 SDK.
"""

from typing import Union
from fastmcp import FastMCP, Context
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("MathMCPServer")

mcp = FastMCP(
    name="Math MCP Server",
    instructions="""
    This server provides basic math tools:
    - add(a, b): Add two numbers.
    - subtract(a, b): Subtract one number from another.
    - explain_calculation(a, b, operation, country): Express the result in words using the selected country's numbering system.
    """
)

@mcp.tool
def add(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Add two numbers.

    Args:
        a (int | float): First operand.
        b (int | float): Second operand.

    Returns:
        float: Sum of a and b.

    Raises:
        ValueError: If inputs are not numbers.
    """
    logger.info(f"Received add request with a={a}, b={b}")
    if not isinstance(a, (int, float)):
        logger.error(f"Invalid type for 'a': {type(a)}")
        raise ValueError("Parameter 'a' must be a number (int or float).")
    if not isinstance(b, (int, float)):
        logger.error(f"Invalid type for 'b': {type(b)}")
        raise ValueError("Parameter 'b' must be a number (int or float).")
    result = float(a) + float(b)
    logger.info(f"add result: {result}")
    return result

@mcp.tool
def subtract(a: Union[int, float], b: Union[int, float]) -> float:
    """
    Subtract b from a.

    Args:
        a (int | float): Value to subtract from.
        b (int | float): Value to subtract.

    Returns:
        float: Result of a - b.

    Raises:
        ValueError: If inputs are not numbers.
    """
    logger.info(f"Received subtract request with a={a}, b={b}")
    if not isinstance(a, (int, float)):
        logger.error(f"Invalid type for 'a': {type(a)}")
        raise ValueError("Parameter 'a' must be a number (int or float).")
    if not isinstance(b, (int, float)):
        logger.error(f"Invalid type for 'b': {type(b)}")
        raise ValueError("Parameter 'b' must be a number (int or float).")
    result = float(a) - float(b)
    logger.info(f"subtract result: {result}")
    return result

@mcp.tool
async def explain_calculation(
    a: Union[int, float],
    b: Union[int, float],
    operation: str,
    country: str,
    ctx: Context
) -> str:
    """
    Use the client's LLM to express the result of the calculation in words,
    using the numbering system of the selected country.

    Args:
        a (int | float): First operand.
        b (int | float): Second operand.
        operation (str): "add" or "subtract"
        country (str): e.g. "US" or "India"
        ctx (Context): MCP context for sampling.

    Returns:
        str: LLM-generated number-in-words description.

    Raises:
        ValueError: If operation is not supported.
    """
    logger.info(f"Received explain_calculation request with a={a}, b={b}, operation={operation}, country={country}")

    # Validate operation.
    if operation not in {"add", "subtract"}:
        logger.error(f"Unsupported operation: {operation}")
        raise ValueError("Operation must be 'add' or 'subtract'.")

    # Calculate the result.
    result = a + b if operation == "add" else a - b

    prompt = (
        f"Express the number {result} in words using the {country} numbering system "
        f"(for example, lakhs and crores for India, millions and billions for US). "
        f"If the number is negative, label it as a negative number."
    )

    try:
        response = await ctx.sample(prompt)
        logger.info(f"LLM response: {response.text}")
        return response.text
    except Exception as e:
        logger.error(f"LLM sampling failed: {e}")
        raise RuntimeError("Failed to generate number in words using LLM.") from e

if __name__ == "__main__":
    logger.info("Starting Math MCP Server on http://127.0.0.1:8080/mcp")
    # The below-mentioned run parameters are not taken into consideration when `fastmcp run` is invoked.
    mcp.run(transport="http", host="127.0.0.1", port=8080)

