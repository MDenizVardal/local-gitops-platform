"""Entrypoint: `python -m shortener`."""

import uvicorn

from shortener.config import load_settings
from shortener.logs import configure_logging
from shortener.main import create_app
from shortener.redis_client import create_redis

configure_logging()
settings = load_settings()
app = create_app(settings, create_redis(settings.redis_url))

# log_config=None keeps uvicorn from replacing our JSON logging. Requests are logged by our
# own middleware, so uvicorn's access log is off.
uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None, access_log=False)
