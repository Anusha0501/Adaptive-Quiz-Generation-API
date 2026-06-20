import time
from redis.asyncio import Redis
from app.core.config import get_settings


class RedisService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = Redis.from_url(self.settings.redis_url, decode_responses=True)

    async def get_cached_quiz(self, key: str) -> str | None:
        return await self.client.get(f"quiz-cache:{key}")

    async def cache_quiz(self, key: str, value: str, ttl_seconds: int = 900) -> None:
        await self.client.setex(f"quiz-cache:{key}", ttl_seconds, value)

    async def save_session(self, session_id: str, payload: str, ttl_seconds: int = 3600) -> None:
        await self.client.setex(f"session:{session_id}", ttl_seconds, payload)

    async def allow_request(self, identity: str) -> bool:
        bucket = f"rate:{identity}:{int(time.time() // 60)}"
        count = await self.client.incr(bucket)
        if count == 1:
            await self.client.expire(bucket, 60)
        return count <= self.settings.rate_limit_per_minute
