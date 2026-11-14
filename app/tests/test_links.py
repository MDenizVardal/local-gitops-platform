def create(client, url="https://example.com/some/long/path"):
    return client.post("/api/links", json={"url": url})


def test_create_returns_code_and_short_url(client):
    response = create(client)

    assert response.status_code == 201
    body = response.json()
    assert body["short_url"] == f"http://short.test/{body['code']}"


def test_create_rejects_invalid_url(client):
    assert create(client, url="not a url").status_code == 422
    assert create(client, url="ftp://example.com/file").status_code == 422


def test_redirect_goes_to_original_url(client):
    code = create(client).json()["code"]

    response = client.get(f"/{code}")

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/some/long/path"


def test_redirect_unknown_code_is_404(client):
    assert client.get("/nope").status_code == 404


def test_link_info_counts_hits(client):
    code = create(client).json()["code"]
    assert client.get(f"/api/links/{code}").json() == {
        "url": "https://example.com/some/long/path",
        "hits": 0,
    }

    client.get(f"/{code}")
    client.get(f"/{code}")

    assert client.get(f"/api/links/{code}").json()["hits"] == 2


def test_link_info_unknown_code_is_404(client):
    assert client.get("/api/links/nope").status_code == 404
