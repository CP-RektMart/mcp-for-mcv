# syntax=docker/dockerfile:1

# 1. Use the official uv image which includes Python and uv
# (Changed from standard python image to ensure 'uv' command works)
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 2. Create a non-privileged user (Security Best Practice)
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/bin/bash" \
    --uid "${UID}" \
    appuser

# Ensure uv can write its cache in a writable location
ENV UV_CACHE_DIR=/app/.cache/uv
RUN mkdir -p "${UV_CACHE_DIR}" && chown -R appuser:appuser /app

# 3. Copy dependency files FIRST (Critical for uv sync)
COPY pyproject.toml uv.lock ./

# 4. Install dependencies as non-root so .venv is owned by appuser
USER appuser
# --frozen: uses the lockfile exactly
# --no-install-project: installs libraries first for caching
RUN uv sync --frozen --no-install-project

# 5. Copy the rest of the source code (as root, but readable by appuser)
USER root
COPY . .

# 6. Install the project itself as appuser (keeps .venv owned by appuser)
USER appuser
RUN uv sync --frozen

# 7. Back to appuser for runtime (explicit, even though already appuser)
USER appuser

# Expose the port
EXPOSE 8000

# Run the application
# IMPORTANT: Ensure src/server.py listens on host="0.0.0.0"
CMD ["uv", "run", "src/server.py"]