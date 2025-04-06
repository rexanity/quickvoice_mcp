from mcp.server.fastmcp import FastMCP
import httpx
import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("QuickVoice-MCP")

# Create an MCP server
mcp = FastMCP("QuickVoice")

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def make_api_call(url: str, payload: Dict, headers: Dict) -> Dict:
    """Make API call with retry logic"""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.ConnectError as e:
        logger.error(f"Connection error to {url}: {str(e)}")
        logger.info("If running in Docker, ensure the API endpoint is accessible from the container")
        raise
    except httpx.HTTPError as e:
        logger.error(f"HTTP error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

@mcp.tool()
def initiate_call(phone_number: str, context: str, instruction: str) -> Dict[str, str]:
    """
    Initiate an outbound call through a QuickVoice agent.
    
    Parameters:
    - phone_number: The phone number to call
    - context: Contextual information needed to complete the tasks for the call, 
        customer account number, address, etc.
    - instruction: Objective of the tasks for the agent to complete the call
    
    Returns:
    - API response data
    """
    call_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    logger.info(f"Initiating call {call_id} to {phone_number}")
    
    # Try to get agent_id from config or environment if not provided
    agent_id = os.environ.get("QUICKVOICE_AGENT_ID")
    if not agent_id:
        logger.error("Missing QUICKVOICE_AGENT_ID environment variable")
        raise ValueError("agent_id must be provided either as a parameter, in MCP config as 'quickvoice.agent_id', or in QUICKVOICE_AGENT_ID environment variable")
    
    # Try to get authorization from config or environment if not provided
    authorization = os.environ.get("QUICKVOICE_API_KEY")
    if not authorization:
        logger.warning("No API key provided in QUICKVOICE_API_KEY")
    
    # Get API endpoint from environment or use default
    api_endpoint = os.environ.get("QUICKVOICE_API_ENDPOINT", "https://api.quickvoice.app")
    url = f"{api_endpoint}/api/calls/initiate"
    logger.debug(f"Using API endpoint: {api_endpoint}")
    
    headers = {}
    if authorization:
        headers["authorization"] = f"Bearer {authorization}"
        logger.debug("Added Bearer token authorization header")
    else:
        logger.error("No authorization token available")
        raise ValueError("API key must be provided in QUICKVOICE_API_KEY environment variable")
    
    payload = {
        "agent_id": agent_id,
        "phone_number": phone_number,
        "context": context,
        "instruction": instruction
    }
    logger.debug(f"Call {call_id} payload prepared")
    
    try:
        result = make_api_call(url, payload, headers)
        logger.info(f"Call {call_id} initiated successfully")
        return result
    except Exception as e:
        error_msg = f"Failed to initiate call {call_id}: {str(e)}"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "status": "failed",
            "call_id": call_id
        }


@mcp.prompt()
def make_outbound_call(
    phone_number: str, 
    context: str = "", 
    instruction: str = "Introduce yourself and ask how you can help."
) -> str:
    """Create a prompt for making an outbound call"""
    logger.info(f"Creating outbound call prompt for {phone_number}")
    logger.debug(f"Context length: {len(context)}, Instruction length: {len(instruction)}")
    
    return f"""
    Please make an outbound call to {phone_number}.
    
    CONTEXT:
    {context}
    
    INSTRUCTION:
    {instruction}
    """


if __name__ == "__main__":
    # Set log level from environment variable or default to INFO
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level))
    
    logger.info("Starting QuickVoice MCP Server")
    logger.info(f"Log level set to {log_level}")
    logger.info(f"API Endpoint: {os.environ.get('QUICKVOICE_API_ENDPOINT', 'http://localhost:8000')}")
    
    # Run the server on default host and port
    mcp.run() 