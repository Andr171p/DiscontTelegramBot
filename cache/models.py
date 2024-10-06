

class RedisUserModel:
    def __init__(
            self, user_id: int, username: str, phone: str
    ) -> None:
        self.user_id = user_id
        self.username = username
        self.phone = phone

    def __repr__(self) -> str:
        return f"RedisUserModel(user_id={self.user_id!r}, username={self.username!r}, phone={self.phone!r}"


class CacheUserModel(RedisUserModel):
    pass
