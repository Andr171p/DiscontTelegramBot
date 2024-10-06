from redis import Redis
from redis import asyncio as aioredis

from cache.settings import RedisLogs

from loguru import logger


class RedisConnection:
    _redis = None

    def __init__(self, url: str) -> None:
        self._url = url

    async def connect(self) -> Redis:
        self._redis = await aioredis.from_url(url=self._url)
        logger.info(RedisLogs.CONNECT_LOG)
        return self._redis

    async def close(self) -> None:
        logger.info(RedisLogs.CLOSE_LOG)
        await self._redis.close()
