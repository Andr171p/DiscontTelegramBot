from cache.set import RedisSetUsers
from cache.get import RedisGetUsers
from cache.cleaner import RedisUsersCleaner
from cache.models import RedisUserModel
from cache.settings import RedisURL


class CacheUsersManager:
    url = RedisURL.REDIS_USERS_URL

    @classmethod
    async def create_cache_user(cls, user: RedisUserModel) -> None:
        redis_set_user = RedisSetUsers(url=cls.url)
        await redis_set_user.set(
            user_id=user.user_id,
            username=user.username,
            phone=user.phone
        )

    @classmethod
    async def get_cache_user(cls, user_id: int) -> RedisUserModel:
        redis_get_user = RedisGetUsers(url=cls.url)
        user = await redis_get_user.get(user_id=user_id)
        return user

    @classmethod
    async def check_cache_user(cls, user_id: int) -> bool:
        redis_get_user = RedisGetUsers(url=cls.url)
        user = await redis_get_user.get(user_id=user_id)
        return True if user.phone is not None else False

    @classmethod
    async def delete_cache_user(cls, user_id: int) -> None:
        redis_user_cleaner = RedisUsersCleaner(url=cls.url)
        await redis_user_cleaner.delete(user_id=user_id)


cache_users_manager = CacheUsersManager()
