from app.config import settings
from app.platforms.base import Platform, PlatformError


class Telegram(Platform):
    name = "Telegram"

    async def post(self, client, message):
        if not (settings.telegram_bot_token and settings.telegram_channel):
            raise PlatformError("not configured: TELEGRAM_BOT_TOKEN / TELEGRAM_CHANNEL")
        r = await client.post(
            f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage",
            json={"chat_id": settings.telegram_channel, "text": message},
        )
        msg = self.check(r)["result"]
        username = msg["chat"].get("username")
        if not username:
            raise PlatformError("channel has no public username, cannot build a public URL")
        return f"https://t.me/{username}/{msg['message_id']}"
