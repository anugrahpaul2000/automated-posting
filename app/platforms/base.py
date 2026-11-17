import httpx


class PlatformError(Exception):
    pass


class Platform:
    """Subclass, set `name`, implement `post` returning the published URL."""

    name = ""

    async def post(self, client: httpx.AsyncClient, message: str) -> str:
        raise NotImplementedError

    @staticmethod
    def check(resp: httpx.Response) -> dict:
        if resp.status_code >= 400:
            raise PlatformError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        return resp.json()
