# app/db/cache.py
#
# Cache layer using Upstash Redis REST API.
# Upstash free tier doesn't support raw TCP Redis connections —
# it uses a simple HTTP REST API instead.
# Docs: https://upstash.com/docs/redis/features/restapi

import httpx
import json
from app.config import get_settings

cfg = get_settings()

HEADERS = {
    "Authorization": f"Bearer {cfg.redis_token}",
    "Content-Type":  "application/json",
}


# ── GET ───────────────────────────────────────────────────────
async def get_cached_packages(cache_key: str) -> dict | None:
    """
    Checks Upstash Redis for a cached TripResponse.
    Returns parsed dict or None if not found / expired.
    """
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(
                f"{cfg.redis_url}/get/pkg:{cache_key}",
                headers=HEADERS,
            )
            r.raise_for_status()
            data = r.json()

        result = data.get("result")
        if not result:
            return None

        return json.loads(result)

    except Exception:
        return None   # cache miss — proceed to fetch


# ── SET ───────────────────────────────────────────────────────
async def store_packages(cache_key: str, data) -> None:
    """
    Stores a TripResponse in Upstash with TTL = CACHE_TTL_SECONDS.
    Uses SETEX command via REST: /setex/key/ttl/value
    """
    try:
        # Serialise — data may be a Pydantic model or plain dict
        if hasattr(data, "model_dump_json"):
            payload = data.model_dump_json()
        else:
            payload = json.dumps(data)

        ttl = cfg.cache_ttl_seconds  # 21600 = 6 hours

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(
                f"{cfg.redis_url}/setex/pkg:{cache_key}/{ttl}",
                headers=HEADERS,
                content=json.dumps(payload),  # value must be JSON string
            )
            r.raise_for_status()

    except Exception as e:
        # Non-fatal — app continues without caching
        print(f"[cache] store failed: {e}")


# ── DELETE ────────────────────────────────────────────────────
async def delete_cached_packages(cache_key: str) -> None:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            await client.get(
                f"{cfg.redis_url}/del/pkg:{cache_key}",
                headers=HEADERS,
            )
    except Exception:
        pass


# ── HEALTH CHECK ──────────────────────────────────────────────
async def ping_cache() -> bool:
    """Returns True if Upstash is reachable. Used in /health endpoint."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(
                f"{cfg.redis_url}/ping",
                headers=HEADERS,
            )
            return r.json().get("result") == "PONG"
    except Exception:
        return False
