from cache.connection import RedisConnection
from cache.utils import mapping


class RedisSetUsers(RedisConnection):
    async def set(self, user_id: int, username: str, phone: str) -> None:
        redis = await self.connect()
        await mapping(
            _redis=redis,
            _user_id=user_id,
            _username=username,
            _phone=phone
        )
        await self.close()
