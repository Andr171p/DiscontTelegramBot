from cache.redis_store.connection import RedisConnection
from cache.redis_store.utils import get_keys
from cache.settings import RedisLogs

from loguru import logger


class RedisUsersCleaner(RedisConnection):
    async def delete(self, user_id: int) -> None:
        redis = await self.connect()
        user_id = str(user_id)
        try:
            await redis.delete(user_id)
            logger.info(RedisLogs.SUCCESSFULLY_DELETE_LOG.format(user_id=user_id))
        except Exception as _ex:
            logger.warning(_ex)
        finally:
            await self.close()

    async def clear(self) -> None:
        redis = await self.connect()
        keys = await get_keys(_redis=redis)
        try:
            await redis.delete(*keys)
            logger.info(RedisLogs.SUCCESSFULLY_CLEAR_LOG)
        except Exception as _ex:
            logger.warning(_ex)
        finally:
            await self.close()