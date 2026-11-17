import re
from typing import List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, field_validator

URL_RE = re.compile(r"https?://\S+", re.I)


class PostRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def check_message(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("message must not be empty")
        if len(v) > 200:
            raise ValueError("message must not exceed 200 characters")
        urls = URL_RE.findall(v)
        if len(urls) != 1:
            raise ValueError("message must contain exactly one CTA link (http/https)")
        u = urlparse(urls[0])
        if not u.hostname or "." not in u.hostname:
            raise ValueError("CTA link is not a valid URL")
        return v


class PlatformResult(BaseModel):
    platform: str
    status: str  # "success" | "failed"
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None


class PostResponse(BaseModel):
    success: bool  # true if at least one platform succeeded
    results: List[PlatformResult]
