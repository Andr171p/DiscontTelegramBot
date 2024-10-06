

class RedisUserModel:
    def __init__(
            self, user_id: bytes | str | int, username: bytes | str, phone: bytes | str
    ) -> None:
        self.user_id = user_id.decode('utf-8')
        self.username = username.decode('utf-8')
        self.phone = phone.decode('utf-8')

    def __repr__(self) -> str:
        return f"RedisUserModel(user_id={self.user_id!r}, username={self.username!r}, phone={self.phone!r}"


class CacheUserModel(RedisUserModel):
    pass
