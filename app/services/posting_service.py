import asyncio
from datetime import datetime

import httpx

from app.platforms import PLATFORMS
from app.schemas import PlatformResult


async def _is_public(client: httpx.AsyncClient, url: str) -> bool:
    try:
        return (await client.get(url, follow_redirects=True)).status_code == 200
    except httpx.HTTPError:
        return False


async def _post_one(client, platform, message) -> PlatformResult:
    try:
        url = await platform.post(client, message)
    except Exception as e:  # one platform failing must never affect the others
        return PlatformResult(platform=platform.name, status="failed", error=str(e) or type(e).__name__)
    now = datetime.now()
    return PlatformResult(
        platform=platform.name,
        status="success",
        posted_url=url,
        public_access=await _is_public(client, url),
        date=now.strftime("%Y-%m-%d"),
        time=now.strftime("%H:%M:%S"),
    )


async def post_everywhere(message: str, platforms=PLATFORMS):
    async with httpx.AsyncClient(timeout=20) as client:
        return await asyncio.gather(*(_post_one(client, p, message) for p in platforms))
