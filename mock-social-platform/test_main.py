from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_publish_is_idempotent():
    payload = {
        "post_id": "test-post",
        "platform": "instagram",
        "caption": "test caption",
        "image_url": "https://example.com/img.png"
    }
    headers = {"Idempotency-Key": "pytest-key-1"}

    first = client.post("/publish", json=payload, headers=headers)
    second = client.post("/publish", json=payload, headers=headers)

    assert first.json()["published_id"] == second.json()["published_id"]


def test_rate_limit_returns_429():
    payload = {
        "post_id": "rate-test",
        "platform": "instagram",
        "caption": "test caption",
        "image_url": "https://example.com/img.png"
    }

    responses = []
    for i in range(6):
        headers = {"Idempotency-Key": f"rate-key-{i}"}
        response = client.post("/publish", json=payload, headers=headers)
        responses.append(response.status_code)

    assert 429 in responses