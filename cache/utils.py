from redis import Redis

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
    _keys = await _redis.keys('*')
    return _keys


async def get_user_data(_redis: Redis, _user_id: int) -> tuple[int, str, str]:
    _username = await _redis.hget(str(_user_id), 'username')
    _phone = await _redis.hget(str(_user_id), 'phone')
    return _user_id, _username, _phone
