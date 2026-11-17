from app.config import settings
from app.platforms.base import Platform, PlatformError


class DevTo(Platform):
    name = "Dev.to"

    async def post(self, client, message):
        if not settings.devto_api_key:
            raise PlatformError("not configured: DEVTO_API_KEY")
        r = await client.post(
            "https://dev.to/api/articles",
            headers={"api-key": settings.devto_api_key},
            json={"article": {"title": message[:80], "body_markdown": message, "published": True}},
        )
        return self.check(r)["url"]
