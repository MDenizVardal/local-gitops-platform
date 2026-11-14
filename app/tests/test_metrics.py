from prometheus_client import REGISTRY


def sample(name, labels=None):
    """Current value of a metric in the default registry, or 0 if it has no samples yet."""
    return REGISTRY.get_sample_value(name, labels or {}) or 0


def test_metrics_endpoint_exposes_prometheus_text(client):
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


def test_business_counters_increase(client):
    created = sample("links_created_total")
    redirects = sample("redirects_total")

    code = client.post("/api/links", json={"url": "https://example.com"}).json()["code"]
    client.get(f"/{code}")

    assert sample("links_created_total") == created + 1
    assert sample("redirects_total") == redirects + 1


def test_requests_are_labelled_by_route_template(client):
    labels = {"method": "GET", "route": "/{code}", "status": "404"}
    before = sample("http_requests_total", labels)

    client.get("/first-unknown")
    client.get("/second-unknown")

    assert sample("http_requests_total", labels) == before + 2
