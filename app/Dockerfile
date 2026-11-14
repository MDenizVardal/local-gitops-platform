# Build stage: install the locked runtime dependencies and the app into /app/.venv.
FROM python:3.15.2-slim-trixie AS build

COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /bin/uv

# Compile .pyc files now, because the runtime filesystem is read-only.
# Use the image's Python instead of downloading another one.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dependencies first, so this layer is cached until pyproject.toml or uv.lock changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY src ./src
RUN uv sync --locked --no-dev --no-editable


# Runtime stage: only Python and the virtualenv. No uv, no build tools, no dev dependencies.
FROM python:3.15.2-slim-trixie

COPY --from=build /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# A numeric non-root user, so Kubernetes can verify runAsNonRoot.
USER 10001:10001
EXPOSE 8000

ENTRYPOINT ["python", "-m", "shortener"]
