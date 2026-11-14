"""The Redis connection used by the routes."""

from redis import Redis


def create_redis(redis_url: str) -> Redis:
    """Build a client that returns strings instead of bytes. It connects on first use."""
    return Redis.from_url(redis_url, decode_responses=True)
