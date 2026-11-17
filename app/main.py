from fastapi import FastAPI

from app.schemas import PostRequest, PostResponse
from app.services.posting_service import post_everywhere

app = FastAPI(title="Automated Multi-Platform Posting")


@app.post("/posting", response_model=PostResponse)
async def posting(req: PostRequest):
    results = await post_everywhere(req.message)
    return PostResponse(success=any(r.status == "success" for r in results), results=results)
