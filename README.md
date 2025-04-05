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

- **Addition Tool**: Adds two numbers together
- **Greeting Resource**: Get a personalized greeting at `greeting://{name}`
- **Initiate Call Tool**: Make outbound calls using QuickVoice AI agents

## Configuration

You can configure your QuickVoice API credentials in one of the following ways:

### 1. MCP Config File

Create an MCP config file at `~/.config/mcp/config.json`:

```json
{
  "quickvoice.agent_id": "your-agent-id",
  "quickvoice.authorization": "your-api-key"
}
```

### 2. Environment Variables

Set the following environment variables:

```bash
export QUICKVOICE_AGENT_ID="your-agent-id"
export QUICKVOICE_API_KEY="your-api-key"
```

### 3. Direct Parameter Passing

Pass credentials directly when calling the function:

```python
response = initiate_call(
    phone_number="1234567890",
    context="Customer call",
    instruction="Follow up on recent order",
    agent_id="your-agent-id",
    authorization="your-api-key"
)
```

## Development

This project uses Poetry for dependency management.

```bash
# Install dependencies
poetry install

# Run the server in development mode
poetry run python -m src.server
```
