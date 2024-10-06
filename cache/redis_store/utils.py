from redis import Redis

from typing import List

from cache.models import RedisUserModel

from misc.utils import timestamp


async def mapping(_redis: Redis, _user_id: int, _username: str, _phone: str) -> None:
    await _redis.hset(
        name=str(_user_id),
        mapping={
            'username': _username,
            'phone': _phone,
            'timestamp': timestamp()
        }
    )


async def get_keys(_redis: Redis) -> list:
    _keys = await _redis.keys("*")
    return _keys


async def get_user_data(_redis: Redis, _user_id: int) -> RedisUserModel:
    _username = await _redis.hget(str(_user_id), 'username')
    _phone = await _redis.hget(str(_user_id), 'phone')
    user = RedisUserModel(
        user_id=_user_id,
        username=_username.decode('utf-8'),
        phone=_phone.decode('utf-8')
    )
    return user


async def get_users_data(_redis: Redis, _keys: list) -> List[RedisUserModel]:
    users = []
    for user_id in _keys:
        _user_id = int(user_id.decode('utf-8'))
        _username = await _redis.hget(user_id, 'username')
        _phone = await _redis.hget(user_id, 'phone')
        users.append(
            RedisUserModel(
                user_id=_user_id,
                username=_username.decode('utf-8'),
                phone=_phone.decode('utf-8')
            )
        )
    return users


class CacheUserSearch:
    def __init__(self, users: List[RedisUserModel]) -> None:
        self.users = users

    def user_id(self, phone: str) -> int | None:
        users = {user.phone: user.user_id for user in self.users}
        user_id = users.get(phone)
        return user_id if phone else None

    def phone(self, user_id: int) -> str | None:
        users = {user.user_id: user.phone for user in self.users}
        phone = users.get(user_id)
        return phone if phone else None
