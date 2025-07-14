ARG UV_VERSION="0.7"
FROM ghcr.io/astral-sh/uv:$UV_VERSION AS uv

FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=uv /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

ENV UV_COMPILE_BYTECODE=1

RUN UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

COPY ./app /app/app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

CMD ["fastapi", "run", "app/main.py"]