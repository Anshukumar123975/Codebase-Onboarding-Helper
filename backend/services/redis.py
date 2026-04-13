import json
import os
from typing import Any

import redis.asyncio as redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_TTL = 60 * 60 * 24  # 24 hours

_pool: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    global _pool
    if _pool is None:
        _pool = redis.from_url(REDIS_URL, decode_responses=True)
    return _pool


async def close_redis():
    global _pool
    if _pool is not None:
        await _pool.aclose()
        _pool = None


# --- job helpers ---

def _job_key(job_id: str) -> str:
    return f"job:{job_id}"


async def create_job(job_id: str, repo_url: str):
    r = await get_redis()
    data = {
        "status": "processing",
        "repo_url": repo_url,
        "current_agent": "",
        "completed_agents": json.dumps([]),
        "progress_percent": 0,
        "result": "",
        "error": "",
    }
    await r.hset(_job_key(job_id), mapping=data)
    await r.expire(_job_key(job_id), CACHE_TTL)


async def update_job(job_id: str, **fields: Any):
    r = await get_redis()
    to_set: dict[str, Any] = {}
    for k, v in fields.items():
        if isinstance(v, (list, dict)):
            to_set[k] = json.dumps(v)
        else:
            to_set[k] = v
    await r.hset(_job_key(job_id), mapping=to_set)


async def get_job(job_id: str) -> dict | None:
    r = await get_redis()
    data = await r.hgetall(_job_key(job_id))
    if not data:
        return None
    data["completed_agents"] = json.loads(data.get("completed_agents", "[]"))
    data["progress_percent"] = int(data.get("progress_percent", 0))
    return data


# --- cache helpers ---

def _cache_key(repo_url: str) -> str:
    return f"cache:{repo_url}"


async def get_cached_result(repo_url: str) -> str | None:
    r = await get_redis()
    return await r.get(_cache_key(repo_url))


async def set_cached_result(repo_url: str, markdown: str):
    r = await get_redis()
    await r.set(_cache_key(repo_url), markdown, ex=CACHE_TTL)
