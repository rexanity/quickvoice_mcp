# QuickVoice MCP

A MCP server to communicate with QuickVoice AI Voice agents.

## Installation

```bash
pip install -e .
```

## Running the Server

Start the MCP server:

```bash
python -m src.server
```

## Available Features

- **Initiate Call Tool**: Make outbound calls using QuickVoice AI agents
  - Calls a phone number with specific context and instructions
  - Includes automatic retry logic for API calls

## Configuration

You can configure your QuickVoice API credentials in one of the following ways:

### 1. Environment Variables

Set the following environment variables:

```bash
export QUICKVOICE_AGENT_ID="your-agent-id"
export QUICKVOICE_API_KEY="your-api-key"
export QUICKVOICE_API_ENDPOINT="http://your-api-endpoint" # Optional, defaults to http://localhost:8000
export LOG_LEVEL="INFO" # Optional, defaults to INFO
```

### 2. MCP Config File

Create an MCP config file by copying the example:

```bash
cp mcp_config.json.example ~/.config/mcp/config.json
```

Then update the values in the config file:

```json
{
  "mcpServers": {
    "QuickVoice": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "QUICKVOICE_AGENT_ID",
        "-e",
        "QUICKVOICE_API_KEY",
        "quickvoice-mcp"
      ],
      "env": {
        "QUICKVOICE_AGENT_ID": "your-agent-id",
        "QUICKVOICE_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Usage Examples

### Initiating a Call

```python
response = initiate_call(
    phone_number="1234567890",
    context="Customer information and relevant details",
    instruction="Ask about their dinner plans"
)
```

## Development

This project uses standard Python dependency management.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server in development mode
python -m src.server
```
