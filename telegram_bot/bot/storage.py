class UserInfoStorage:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.phone_number = None

    def add(self, telegram_user_id, telegram_username, telegram_phone_number):
        self.user_id = telegram_user_id
        self.username = telegram_username
        self.phone_number = telegram_phone_number

    def data(self):
        return [self.user_id, self.username, self.phone_number]

    def clear_storage(self):
        self.user_id = None
        self.username = None
        self.phone_number = None
