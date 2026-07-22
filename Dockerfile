FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies (leverages Docker layer caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# Copy project
COPY . .

# Use the venv uv created
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["sh", "debug.sh"]
