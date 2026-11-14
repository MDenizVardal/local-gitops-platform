def test_version_returns_app_version(client):
    assert client.get("/api/version").json() == {"version": "test-sha"}


def test_healthz_is_ok(client):
    assert client.get("/healthz").status_code == 200


def test_readyz_is_ok_when_redis_answers(client):
    assert client.get("/readyz").status_code == 200


def test_readyz_is_503_when_redis_is_down(client, redis_server):
    redis_server.connected = False

    assert client.get("/readyz").status_code == 503


def test_healthz_stays_ok_when_redis_is_down(client, redis_server):
    redis_server.connected = False

    assert client.get("/healthz").status_code == 200
