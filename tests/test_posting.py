import pytest
from fastapi.testclient import TestClient

from app import main
from app.platforms.base import Platform, PlatformError
from app.services import posting_service

client = TestClient(main.app)
URL = "https://example.com"


@pytest.mark.parametrize("msg", [
    "no link here",
    f"two links {URL} and {URL}/b",
    "x" * 190 + f" {URL}",
    "bad link http://localhost",
    "   ",
])
def test_invalid_messages_rejected(msg):
    assert client.post("/posting", json={"message": msg}).status_code == 422


class Good(Platform):
    name = "Good"

    async def post(self, c, m):
        return "https://example.com/p/1"


class Bad(Platform):
    name = "Bad"

    async def post(self, c, m):
        raise PlatformError("Authentication failed")


def test_failure_isolated(monkeypatch):

    async def no_net(c, u):
        return True

    monkeypatch.setattr(posting_service, "_is_public", no_net)
    orig = posting_service.post_everywhere

    async def patched(message):
        return await orig(message, [Good(), Bad()])

    monkeypatch.setattr(main, "post_everywhere", patched)
    body = client.post("/posting", json={"message": f"hi {URL}"}).json()
    assert body["success"] is True
    good, bad = body["results"]
    assert good["status"] == "success" and good["public_access"] and good["date"]
    assert bad["status"] == "failed" and bad["error"] == "Authentication failed"
