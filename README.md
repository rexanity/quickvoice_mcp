![Image](https://github.com/user-attachments/assets/5948811b-0265-4e48-809a-7dca01839905)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Available-blue.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/rexanity/quickvoice-mcp)

# QuickVoice MCP

A MCP server to communicate with QuickVoice AI Voice agents.

## 🚀 Quickstart

1. Get your QuickVoice API credentials (agent ID and API key)
2. Set up Claude Desktop with QuickVoice MCP
3. Start making AI phone calls with natural language prompts

## QuickVoice.app Web Interface

### Accessing the Dashboard
1. Go to [quickvoice.app](https://quickvoice.app) and sign in with your credentials
2. Navigate to the Dashboard to view your agent status, call history, and credit usage
3. Access the Settings page to manage your API keys and agent configuration

### Managing Your Agent
- **Create/Edit Agent**: Configure your agent's voice, behavior, and response patterns
- **Conversation History**: Review past calls and analyze conversation transcripts
- **Analytics**: Track call performance metrics and user engagement

### Getting API Credentials
1. Go to Settings > API
2. Generate a new API key if you don't have one
3. Copy your Agent ID and API Key to use with the MCP integration

## 📱 Using with Claude Desktop

### Claude Desktop Setup

1. Open Claude Desktop
2. Go to Settings > Developer > Edit Config
3. Add the following to your `claude_desktop_config.json`:

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
        "rexanity/quickvoice-mcp"
      ],
      "env": {
        "QUICKVOICE_AGENT_ID": "your-agent-id",
        "QUICKVOICE_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Example Prompts

Try asking Claude:

- "Call 555-123-4567 and schedule an appointment for tomorrow at 2pm"
- "Call my customer to follow up on their order status"
- "Make a call to check if a restaurant has availability for dinner tonight"
- "Call this number and ask about their business hours"

<img width="856" alt="Image" src="https://github.com/user-attachments/assets/c88fadd4-5789-43d9-8203-1118f45f0b49" />

⚠️ **Note**: Using QuickVoice will consume API credits based on your account's billing terms.

For detailed instructions on integrating QuickVoice with Claude Desktop, see [CLAUDE_DESKTOP.md](CLAUDE_DESKTOP.md).

## Installation Options

### Docker (Recommended)

```bash
# Pull the Docker image
docker pull rexanity/quickvoice-mcp

# Run the container
docker run -e QUICKVOICE_AGENT_ID="your-agent-id" -e QUICKVOICE_API_KEY="your-api-key" rexanity/quickvoice-mcp
```

### Using Pip

```bash
pip install -e .
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
        "rexanity/quickvoice-mcp"
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

## 🔧 Development

### Poetry Setup

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell

# Run the server in development mode
poetry run python -m src.server
```

### Docker Development

```bash
# Build the development image locally
docker build -t quickvoice-mcp-dev --target development .

# Run with mounted source code for live reloading
docker run -v $(pwd):/app -e QUICKVOICE_AGENT_ID="your-agent-id" -e QUICKVOICE_API_KEY="your-api-key" -e QUICKVOICE_API_ENDPOINT="http://host.docker.internal:8000" quickvoice-mcp-dev
```

> Note: While the `:latest` tag is implied when no tag is specified, using explicit tags (like `:dev` or `:1.0.0`) is recommended for production environments to ensure version stability.

## 🔍 Troubleshooting

### Log Locations
- **macOS**: `~/Library/Logs/Claude/mcp-server-quickvoice.log`
- **Windows**: `%APPDATA%\Claude\logs\mcp-server-quickvoice.log`

### Common Issues

#### API Connection Errors
- Verify your API credentials are correct
- Check that your API endpoint is reachable from your environment
- For Docker: ensure `host.docker.internal` is used for local development

#### Call Not Initiating
- Confirm the phone number format is correct (include country code if necessary)
- Ensure your QuickVoice account has sufficient credits
- Check the API response for specific error messages
