from cache.redis_store.connection import RedisConnection
from cache.models import RedisUserModel
from cache.settings import RedisLogs
from cache.redis_store.utils import (
    get_keys,
    get_user_data,
    get_users_data
)

from loguru import logger

from typing import List


class RedisGetUsers(RedisConnection):
    async def get(self, user_id: int) -> RedisUserModel:
        redis = await self.connect()
        user = await get_user_data(
            _redis=redis,
            _user_id=user_id
        )
        logger.info(RedisLogs.GET_USER_LOG.format(user=user))
        await self.close()
        return user

    async def get_all(self) -> List[RedisUserModel]:
        redis = await self.connect()
        keys = await get_keys(_redis=redis)
        users = await get_users_data(
            _redis=redis,
            _keys=keys
        )
        logger.info(RedisLogs.GET_USERS_LOG.format(users=users))
        await self.close()
        return users
