"""HTTP endpoints."""

import secrets

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from redis import Redis, RedisError

from shortener.metrics import LINKS_CREATED, REDIRECTS, metrics_response

router = APIRouter()


class CreateLink(BaseModel):
    url: HttpUrl


def _key(code: str) -> str:
    return f"link:{code}"


def _redis(request: Request) -> Redis:
    return request.app.state.redis


@router.get("/healthz")
def healthz() -> dict:
    """Liveness: the process is up. No dependency checks, so a Redis outage never restarts us."""
    return {"status": "ok"}


@router.get("/readyz")
def readyz(request: Request) -> dict:
    """Readiness: we can serve traffic only if Redis answers."""
    try:
        _redis(request).ping()
    except RedisError as error:
        raise HTTPException(status_code=503, detail="redis unreachable") from error
    return {"status": "ready"}


@router.get("/metrics")
def metrics() -> Response:
    return metrics_response()


@router.get("/api/version")
def version(request: Request) -> dict:
    return {"version": request.app.state.settings.app_version}


@router.post("/api/links", status_code=201)
def create_link(body: CreateLink, request: Request) -> dict:
    redis = _redis(request)
    # HSETNX only writes if the field is new, so a code that is already taken is never overwritten.
    while True:
        code = secrets.token_urlsafe(5)
        if redis.hsetnx(_key(code), "url", str(body.url)):
            break
    LINKS_CREATED.inc()
    return {"code": code, "short_url": f"{request.app.state.settings.base_url}/{code}"}


@router.get("/api/links/{code}")
def link_info(code: str, request: Request) -> dict:
    link = _redis(request).hgetall(_key(code))
    if not link:
        raise HTTPException(status_code=404, detail="unknown code")
    return {"url": link["url"], "hits": int(link.get("hits", 0))}


# Registered last: "/{code}" would otherwise also match "/healthz", "/readyz" and "/metrics".
@router.get("/{code}")
def follow(code: str, request: Request) -> RedirectResponse:
    redis = _redis(request)
    url = redis.hget(_key(code), "url")
    if url is None:
        raise HTTPException(status_code=404, detail="unknown code")
    redis.hincrby(_key(code), "hits", 1)
    REDIRECTS.inc()
    return RedirectResponse(url, status_code=307)
