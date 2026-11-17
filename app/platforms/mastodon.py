from app.config import settings
from app.platforms.base import Platform, PlatformError


class Mastodon(Platform):
    name = "Mastodon"

    async def post(self, client, message):
        if not settings.mastodon_token:
            raise PlatformError("not configured: MASTODON_TOKEN")
        r = await client.post(
            f"{settings.mastodon_base_url.rstrip('/')}/api/v1/statuses",
            headers={"Authorization": f"Bearer {settings.mastodon_token}"},
            data={"status": message, "visibility": "public"},
        )
        return self.check(r)["url"]
