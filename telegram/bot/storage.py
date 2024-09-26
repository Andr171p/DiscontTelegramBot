class UserInfoStorage:
    user_id = None
    username = None
    phone = None

    def __repr__(self):
        return f"(user_id={self.user_id}, username={self.username}, phone={self.phone})"

    @classmethod
    def add(cls, user_id, username, phone):
        cls.user_id = user_id
        cls.username = username
        cls.phone = phone

    @classmethod
    def data(cls):
        return {
            "user_id": cls.user_id,
            "username": cls.username,
            "phone": cls.phone
        }

    @classmethod
    def clear(cls):
        cls.user_id = None
        cls.username = None
        cls.phone = None


user_info_storage = UserInfoStorage()
