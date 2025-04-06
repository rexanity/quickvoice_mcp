# QuickVoice for Claude Desktop

This guide will help you set up QuickVoice MCP to work with Claude Desktop, allowing Claude to make phone calls for you.

## Setting up Claude Desktop

1. Download and install [Claude Desktop](https://claude.ai/desktop) for macOS or Windows.
2. Make sure you have the latest version by clicking on the Claude menu and selecting "Check for Updates..."
3. Ensure Docker is installed and running on your computer, as QuickVoice MCP runs in a Docker container.

## Installing Docker (for Non-Developers)

If you don't have Docker installed, follow these steps:

### For macOS:
1. Download Docker Desktop from [Docker's website](https://www.docker.com/products/docker-desktop/)
2. Double-click the downloaded `.dmg` file to open the installer
3. Drag the Docker icon to the Applications folder
4. Open Docker from your Applications folder
5. You might be asked to provide administrator permissions
6. Wait for Docker to start (the Docker icon in the menu bar will stop animating when it's ready)

### For Windows:
1. Download Docker Desktop from [Docker's website](https://www.docker.com/products/docker-desktop/)
2. Double-click the installer (.exe file)
3. Follow the installation wizard instructions
4. When prompted, ensure the "Use WSL 2 instead of Hyper-V" option is selected (recommended)
5. Click "OK" to begin the installation
6. After installation, start Docker Desktop from the Start menu
7. Wait for Docker to start (the Docker icon in the system tray will stop animating when it's ready)

### Verifying Docker Installation:
To verify Docker is running properly:
1. Open Terminal (macOS) or Command Prompt (Windows)
2. Type `docker --version` and press Enter
3. If Docker is installed correctly, you should see the Docker version number

## Configuring Claude Desktop

1. Open the Claude menu and select "Settings..."
2. Click on "Developer" in the left-hand bar, then click on "Edit Config"
3. This will open or create a configuration file at:
   * macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   * Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Adding QuickVoice MCP

Add the following configuration to your Claude Desktop config file:

### MacOS Configuration

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

### Windows Configuration

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

## Getting Your API Credentials

To use QuickVoice, you'll need:

1. A QuickVoice agent ID
2. A QuickVoice API key

Replace the placeholders in the configuration above with your actual credentials.

## Preparing Docker for QuickVoice (One-Time Setup)

Before using QuickVoice with Claude Desktop, you need to pull the QuickVoice Docker image. This is a one-time setup:

1. Open Terminal (macOS) or Command Prompt (Windows)
2. Copy and paste this command:
   ```
   docker pull rexanity/quickvoice-mcp
   ```
3. Press Enter and wait for Docker to download the image
4. You should see progress bars as Docker downloads the image
5. When complete, you'll see a message indicating the download is done

This step ensures the QuickVoice image is available on your computer before Claude Desktop tries to use it.

## Restart Claude

After updating your configuration file, restart Claude Desktop completely:

1. Close Claude Desktop
2. Reopen Claude Desktop
3. You should see a hammer icon in the bottom right corner of the input box
4. When you click the hammer icon, QuickVoice should appear in the tools list

## Using QuickVoice with Claude

You can now ask Claude to make phone calls for you. Examples:

* "Call 555-123-4567 and ask what time they're going to dinner"
* "Call my doctor and schedule an appointment"
* "Call this number and take a message"

Claude will use QuickVoice to make the call and will ask for your approval before executing the action.

## Troubleshooting

If the server doesn't show up in Claude:

1. Make sure Docker is running on your system
2. Verify your API credentials are correct
3. Check your configuration file syntax
4. Restart Claude Desktop completely
5. Look at Claude Desktop logs:
   * macOS: `~/Library/Logs/Claude`
   * Windows: `%APPDATA%\Claude\logs`
   * Check `mcp.log` and `mcp-server-QuickVoice.log`

## Advanced Configuration

You can modify the Docker configuration to specify the API endpoint:

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
        "-e",
        "QUICKVOICE_API_ENDPOINT",
        "rexanity/quickvoice-mcp"
      ],
      "env": {
        "QUICKVOICE_AGENT_ID": "your-agent-id",
        "QUICKVOICE_API_KEY": "your-api-key",
        "QUICKVOICE_API_ENDPOINT": "http://your-api-endpoint"
      }
    }
  }
}
```

For more details on MCP integration with Claude Desktop, visit the [Model Context Protocol documentation](https://modelcontextprotocol.io/quickstart/user).

## How It Works (For Non-Developers)

When you use QuickVoice with Claude Desktop:

1. **Docker** is a platform that runs applications in containers. Think of it like a lightweight virtual computer that only runs one program.

2. When you ask Claude to make a phone call, Claude Desktop communicates with the QuickVoice MCP server running in Docker.

3. You'll see a confirmation prompt before any call is made, so you're always in control.

4. The Docker container handles all the technical details of connecting to the phone system.

5. You don't need to keep Terminal/Command Prompt open after pulling the Docker image - Claude Desktop will automatically start the container when needed.

If you ever want to stop using QuickVoice:
1. Open the Claude Desktop configuration file
2. Delete or comment out the QuickVoice section
3. Restart Claude Desktop 