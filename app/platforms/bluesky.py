import re
from datetime import datetime, timezone

from app.config import settings
from app.platforms.base import Platform, PlatformError

PDS = "https://bsky.social/xrpc"


class Bluesky(Platform):
    name = "Bluesky"

    async def post(self, client, message):
        if not (settings.bluesky_handle and settings.bluesky_app_password):
            raise PlatformError("not configured: BLUESKY_HANDLE / BLUESKY_APP_PASSWORD")
        session = self.check(await client.post(
            f"{PDS}/com.atproto.server.createSession",
            json={"identifier": settings.bluesky_handle, "password": settings.bluesky_app_password},
        ))
        record = {
            "$type": "app.bsky.feed.post",
            "text": message,
            "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        # Make the link clickable: facets use UTF-8 byte offsets.
        m = re.search(r"https?://\S+", message)
        if m:
            start = len(message[: m.start()].encode())
            record["facets"] = [{
                "index": {"byteStart": start, "byteEnd": start + len(m.group().encode())},
                "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group()}],
            }]
        created = self.check(await client.post(
            f"{PDS}/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {session['accessJwt']}"},
            json={"repo": session["did"], "collection": "app.bsky.feed.post", "record": record},
        ))
        rkey = created["uri"].rsplit("/", 1)[-1]
        return f"https://bsky.app/profile/{session['handle']}/post/{rkey}"
