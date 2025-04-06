# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies and poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to PATH
ENV PATH="/root/.local/bin:$PATH"
RUN pip install pipx
RUN pipx install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment (not needed in Docker)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Create log directory
RUN mkdir -p /var/log/quickvoice-mcp

# Copy source code
COPY src/ ./src/

# Set environment variables (these can be overridden at runtime)
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO
ENV LOG_DIR=/var/log/quickvoice-mcp

# Create volume for logs
VOLUME ["/var/log/quickvoice-mcp"]

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f ${QUICKVOICE_API_ENDPOINT}/health || exit 1

# Run the MCP server
CMD ["poetry", "run", "python", "-m", "src.server"] 