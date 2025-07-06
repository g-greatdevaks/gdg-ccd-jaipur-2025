"""
Streamlit Host App for FastMCP 2.0 Math Server

Features:
- Arithmetic operations (add and subtract)
- LLM-powered number-in-words explanation (country-specific)
- Barcode generation via Cloud Run MCP Server (optional)
- Robust error handling and user feedback
"""

import streamlit as st
import asyncio
import logging
from fastmcp import Client
from fastmcp.client.sampling import SamplingMessage, SamplingParams, RequestContext
import google.generativeai as genai
import os
from typing import Optional, Any, Dict

# ---- Logging setup ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("HostApp")

# ---- MCP server URLs ----
MCP_SERVER_URL: str = "http://localhost:8080/mcp"
CLOUDRUN_MCP_URL: str = "http://localhost:8081/mcp"  # Cloud Run Proxy URL.

# ---- Gemini API Key ----
GEMINI_API_KEY: Optional[str] = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set your Gemini API key in Streamlit secrets or as an environment variable.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    ctx: RequestContext,
) -> str:
    """
    Handles LLM sampling requests from the MCP server using Gemini.
    """
    prompt: str = ""
    for m in messages:
        if m.content.type == "text":
            prompt = m.content.text
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini LLM call failed: {e}")
        return "LLM error: Could not generate number in words."

async def call_tool(
    tool: str, 
    a: Any, 
    b: Any, 
    operation: Optional[str] = None, 
    country: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calls an MCP tool and returns the result or error.
    """
    async with Client(MCP_SERVER_URL, sampling_handler=sampling_handler) as client:
        logger.info(f"Calling tool '{tool}' with a={a!r}, b={b!r}, operation={operation!r}, country={country!r}")
        try:
            params = {"a": a, "b": b}
            if tool == "explain_calculation":
                params["operation"] = operation
                params["country"] = country
            result = await client.call_tool(tool, params)
            logger.info(f"Result: {result}")
            return {"success": True, "result": result, "raw_response": result}
        except Exception as e:
            logger.error(f"Error calling tool: {e}")
            return {"success": False, "error": str(e), "raw_response": str(e)}

async def get_barcode_from_cloudrun(number: int, barcode_type: str = "qr") -> Optional[str]:
    """
    Calls the Cloud Run MCP server to generate a barcode image URL.

    Args:
        number (int): The number to encode.
        barcode_type (str): The type of barcode.

    Returns:
        Optional[str]: The barcode image URL, or None if error.
    """
    try:
        async with Client(CLOUDRUN_MCP_URL) as client:
            response = await client.call_tool("generate_barcode", {"number": number, "type": barcode_type})
            return response.data.get("barcode_url")
    except Exception as e:
        logger.error(f"Error fetching barcode from Cloud Run MCP server: {e}")
        return None

def try_cast(val: str) -> Any:
    """
    Try to cast to int or float, else return as string.
    """
    try:
        if "." in val:
            return float(val)
        else:
            return int(val)
    except Exception:
        return val  # Send as string if not a number.

async def perform_calculation(
    tool: str,
    a_val: Any,
    b_val: Any,
    operation: Optional[str],
    country: Optional[str],
    explain: bool,
    barcode_toggle: bool,
    barcode_type: str,
) -> Dict[str, Any]:
    """
    Performs the Math/LLM call and, if requested, barcode generation.
    """
    # Math/LLM.
    if explain:
        response = await call_tool("explain_calculation", a_val, b_val, operation, country)
    else:
        response = await call_tool(operation, a_val, b_val)

    # Barcode (optional).
    barcode_url = None
    if barcode_toggle and response["success"]:
        if explain:
            numeric_result = a_val + b_val if operation == "add" else a_val - b_val
        else:
            numeric_result = response['result'].data
        barcode_url = await get_barcode_from_cloudrun(numeric_result, barcode_type)

    return {"response": response, "barcode_url": barcode_url}

st.title("FastMCP Number-in-Words Demo (with Gemini LLM & Cloud Run-based Barcode Generator)")

# --- UI widgets ---
explain: bool = st.checkbox("Express the result in words (LLM)")
country: Optional[str] = None
if explain:
    country = st.selectbox("Country", ["US", "India"])

barcode_toggle: bool = st.checkbox("Show Barcode using Cloud Run")
barcode_type: Optional[str] = None
if barcode_toggle:
    barcode_type = st.selectbox("Barcode Type", ["qr", "code128", "code39", "ean13"])

# --- Form for numbers and operation ---
with st.form("math_form"):
    a_str: str = st.text_input("First number (a)", value="")
    b_str: str = st.text_input("Second number (b)", value="")
    operation: str = st.selectbox("Operation", ["add", "subtract"])
    submitted: bool = st.form_submit_button("Calculate")

if submitted:
    if not a_str.strip() or not b_str.strip():
        st.error("Please enter values for both numbers.")
    elif explain and not country:
        st.error("Please select a country for the number-in-words explanation.")
    else:
        a_val = try_cast(a_str.strip())
        b_val = try_cast(b_str.strip())

        # Run all async work in one event loop
        result = asyncio.run(
            perform_calculation(
                operation,
                a_val,
                b_val,
                operation,
                country,
                explain,
                barcode_toggle,
                barcode_type,
            )
        )

        response = result["response"]
        barcode_url = result["barcode_url"]

        # Show result
        if response["success"]:
            if explain:
                st.success(f"Number in words: {response['result'].data}")
            else:
                st.success(f"Result: {response['result'].data}")
        else:
            st.error(f"Calculation failed: {response.get('error', '')}")

        # Always show full response or error from MCP server.
        st.markdown("**Full MCP Server Response/Error:**")
        st.code(str(response["raw_response"]))

        # Barcode display.
        if barcode_toggle and response["success"]:
            if barcode_url:
                if explain:
                    numeric_result = a_val + b_val if operation == "add" else a_val - b_val
                else:
                    numeric_result = response['result'].data
                st.image(barcode_url, caption=f"Barcode for {numeric_result}")
            else:
                st.error("Could not generate barcode from Cloud Run MCP server.")
