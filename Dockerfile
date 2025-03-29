FROM python:3.12-slim

# intslling system dependencies for LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# install uv accoding to the documentation: https://docs.astral.sh/uv/guides/integration/fastapi/#deployment
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

ENV PYTHONPATH=/app

# runing the application using the uvicorn according to doc mentioned previously
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "src.api.main_api:app", "--host", "0.0.0.0", "--port", "8080"]
