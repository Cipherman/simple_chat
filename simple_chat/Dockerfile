FROM python:3.12-slim-trixie

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Set working directory
WORKDIR /app

# Copy config from the root (the context)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Copy everything from your context into the container
COPY . .

# Disable development dependencies
ENV UV_NO_DEV=1

# Sync the project into a new environment, asserting the lockfile is up to date
RUN uv sync --locked

# Set OLLAMA_BASE_URL to use the Ollama container name when on the same Docker network
# Default assumes the Ollama container is named 'ollama-server' (matches docker-compose.yml)
# Override with: docker run -e OLLAMA_BASE_URL=http://your-ollama-container-name:11434/v1
ENV OLLAMA_BASE_URL=http://ollama-server:11434/v1

# Set the default command to run the application
# app.py is in simple_chat/ directory relative to the build context (root)
CMD ["uv", "run", "streamlit", "run", "simple_chat/app.py"]