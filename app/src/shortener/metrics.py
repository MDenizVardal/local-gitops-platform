"""Prometheus metrics and the middleware that records every request."""

import logging
import time

from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

log = logging.getLogger("shortener.request")

REQUESTS = Counter(
    "http_requests_total",
    "HTTP requests by method, route template and status code.",
    ["method", "route", "status"],
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration by method, route template and status code.",
    ["method", "route", "status"],
)
LINKS_CREATED = Counter("links_created_total", "Short links created.")
REDIRECTS = Counter("redirects_total", "Redirects served.")


async def record_request(request: Request, call_next) -> Response:
    """Time the request, then count it and log it under its route template."""
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    # The route template ("/{code}") keeps label values few. The raw path would not.
    route = request.scope["route"].path if "route" in request.scope else "unmatched"
    status = str(response.status_code)
    REQUESTS.labels(request.method, route, status).inc()
    LATENCY.labels(request.method, route, status).observe(duration)
    log.info(
        "request",
        extra={
            "method": request.method,
            "route": route,
            "status": response.status_code,
            "duration_ms": round(duration * 1000, 2),
        },
    )
    return response


def metrics_response() -> Response:
    """Render all metrics in the Prometheus text format."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
