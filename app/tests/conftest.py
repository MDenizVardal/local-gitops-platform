import pytest
from fakeredis import FakeRedis, FakeServer
from fastapi.testclient import TestClient

from shortener.config import Settings
from shortener.main import create_app

SETTINGS = Settings(
    redis_url="redis://unused", base_url="http://short.test", app_version="test-sha"
)


@pytest.fixture
def redis_server() -> FakeServer:
    """An in-memory Redis. Setting `connected = False` on it simulates an outage."""
    return FakeServer()


@pytest.fixture
def client(redis_server: FakeServer) -> TestClient:
    redis = FakeRedis(server=redis_server, decode_responses=True)
    return TestClient(create_app(SETTINGS, redis), follow_redirects=False)
