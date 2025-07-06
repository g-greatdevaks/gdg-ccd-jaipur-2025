"""
Barcode Generator MCP Server using FastMCP 2.0

This server leverages FastMCP 2.0 and exposes
a tool to generate a barcode for the number
fed to it.
"""

import logging
from fastmcp import FastMCP
from typing import Dict

# Configure logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("CloudRunMCPServer")

mcp = FastMCP(name="CloudRun Barcode Server")

@mcp.tool
def generate_barcode(number: int, type: str = "qr") -> Dict[str, str]:
    """
    Generate a barcode image URL for the given number.

    Args:
        number (int): The number to encode in the barcode.
        type (str, optional): The barcode type. Defaults to 'qr'.
            Allowed: 'qr', 'code128', 'code39', 'ean13'.

    Returns:
        Dict[str, str]: A dictionary with the barcode image URL.
    """
    allowed_types = {"qr", "code128", "code39", "ean13"}
    if type not in allowed_types:
        logger.warning(f"Invalid barcode type '{type}', defaulting to 'qr'.")
        type = "qr"
    url = f"https://barcode.orcascan.com/?data={number}&type={type}"
    logger.info(f"Generated barcode URL for number {number}: {url}")
    return {"barcode_url": url}

if __name__ == "__main__":
    logger.info("Starting CloudRun Barcode MCP Server on 0.0.0.0:8080")
    # The below-mentioned run parameters are not taken into consideration when `fastmcp run` is invoked.
    mcp.run(transport="http", host="0.0.0.0", port=8080)
