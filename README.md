# Automated Multi-Platform Posting

FastAPI service with one endpoint, `POST /posting`, that publishes a short message to five platforms in parallel. A failure on one platform never affects the others.

| Platform | API | Credential |
|---|---|---|
| Mastodon | `POST /api/v1/statuses` | access token with `write:statuses` |
| Bluesky | AT Protocol `createSession` + `createRecord` | handle + app password |
| Dev.to | Forem `POST /api/articles` | API key |
| Telegram | Bot API `sendMessage` (public channel) | bot token, bot must be channel admin |
| Discord | Webhook `?wait=true` | webhook URL |

Platforms without credentials are reported as `failed` with `not configured: ...`.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in the credentials you have
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

Docs: http://localhost:4000/docs. Tests: `pytest`.

## Validation

The message must be at most 200 characters, non-empty, and contain exactly one http(s) link with a valid host. Otherwise the API returns `422`.

## Example

```bash
curl -X POST http://localhost:4000/posting -H 'content-type: application/json' \
  -d '{"message": "Grow your online visibility https://example.com"}'
```

```json
{
  "success": true,
  "results": [
    {"platform": "Mastodon", "status": "success", "posted_url": "https://mastodon.social/@user/1130000000000000", "public_access": true, "date": "2026-11-17", "time": "10:30:00", "error": null},
    {"platform": "Dev.to", "status": "failed", "posted_url": null, "public_access": false, "date": null, "time": null, "error": "not configured: DEVTO_API_KEY"}
  ]
}
```

(Illustrative.) Invalid input:

```json
{"detail": [{"loc": ["body", "message"], "msg": "Value error, message must contain exactly one CTA link (http/https)"}]}
```

`success` is `true` if at least one platform succeeded. `public_access` is checked with an unauthenticated GET on the posted URL. Discord server channels are members-only, so it will report `false`.

## Layout

`app/main.py` endpoint, `app/schemas.py` validation and models, `app/config.py` env settings, `app/platforms/` one small class per platform, `app/services/posting_service.py` concurrent fan-out and result handling.
