FROM python:3.13-slim

WORKDIR /app

ENV UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

COPY ./app /app/app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-groups

# Run with fastapi
CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app", "--reload"]
