from app.platforms.bluesky import Bluesky
from app.platforms.devto import DevTo
from app.platforms.discord import Discord
from app.platforms.mastodon import Mastodon
from app.platforms.telegram import Telegram

PLATFORMS = [Mastodon(), Bluesky(), DevTo(), Telegram(), Discord()]
