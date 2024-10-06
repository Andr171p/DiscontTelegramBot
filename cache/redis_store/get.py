from cache.redis_store.connection import RedisConnection
from cache.models import RedisUserModel
from cache.settings import RedisLogs
from cache.redis_store.utils import get_user_data

from loguru import logger


class RedisGetUsers(RedisConnection):
    async def get(self, user_id: int) -> RedisUserModel:
        redis = await self.connect()
        user_id, username, phone = await get_user_data(
            _redis=redis,
            _user_id=user_id
        )
        user = RedisUserModel(
            user_id=user_id,
            username=username.decode('utf-8'),
            phone=phone.decode('utf-8')
        )
        await self.close()
        logger.info(RedisLogs.GET_USER_LOG.format(user=user))
        return user
