"""
Streamlit Host App for FastMCP 2.0 Math Server

Features:
- Arithmetic operations (add and subtract)
- LLM-powered number-in-words explanation (country-specific)
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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("HostApp")

MCP_SERVER_URL: str = "http://localhost:8080/mcp"

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

st.title("FastMCP Number-in-Words Demo (with Gemini LLM)")

# --- Instant UI widgets ---
explain: bool = st.checkbox("Express the result in words (LLM)")
country: Optional[str] = None
if explain:
    country = st.selectbox("Country", ["US", "India"])

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

        if explain:
            response = asyncio.run(call_tool("explain_calculation", a_val, b_val, operation, country))
        else:
            response = asyncio.run(call_tool(operation, a_val, b_val))

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
