"""Builds the FastAPI application."""

from fastapi import FastAPI
from redis import Redis

from shortener.config import Settings
from shortener.metrics import record_request
from shortener.routes import router


def create_app(settings: Settings, redis: Redis) -> FastAPI:
    """Wire settings, Redis, metrics and routes together. Tests pass in a fake Redis."""
    app = FastAPI(title="shortener", version=settings.app_version)
    app.state.settings = settings
    app.state.redis = redis
    app.middleware("http")(record_request)
    app.include_router(router)
    return app
