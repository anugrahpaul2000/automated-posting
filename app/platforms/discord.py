from app.config import settings
from app.platforms.base import Platform, PlatformError


class Discord(Platform):
    name = "Discord"

    async def post(self, client, message):
        url = settings.discord_webhook_url
        if not url:
            raise PlatformError("not configured: DISCORD_WEBHOOK_URL")
        msg = self.check(await client.post(url, params={"wait": "true"}, json={"content": message}))
        guild = self.check(await client.get(url)).get("guild_id")
        # Server channels are members-only, so public_access will be reported as false.
        return f"https://discord.com/channels/{guild}/{msg['channel_id']}/{msg['id']}"
