class Messages:
    START_MESSAGE = "Здравствуйте, {username}! Вам нужно пройти регистрацию. Это займёт всего пару секунд"
    ALREADY_REGISTER_MESSAGE = "Вы уже зарегистрированы..."
    START_REGISTER_MESSAGE = "Для регистрации просто введите свой номер телефона"
    SUCCESS_REGISTER_MESSAGE = "Вы успешно зарегистрированы"
    CHECK_PHONE_NUMBER_MESSAGE = "Это ваш номер телефона?\n"
    INPUT_PHONE_NUMBER_MESSAGE = ("Введите свой номер телефона начиная с цифры '7'\n"
                                  "Пример: <b>79998885533</b>")
    SEARCH_ORDER_MESSAGE = "Идёт поиск заказа..."
    EMPTY_ORDER_MESSAGE = "У вас пока нет заказа..."
    PROBLEM_STATUS_MESSAGE = ("Из за чего это может быть?\n"
                              "<b>- Возможно у вас ещё нет заказа</b>\n"
                              "<b>- Заказ ещё не принят оператором</b>\n"
                              "(нужно подождать пару минут)\n"
                              "<b>- При регистрации был указан не правильный номер телефона</b>")
    WAIT_STATUS_MESSAGE = "Попробуйте отправить запрос через 5-7 минут"
    PHONE_QUESTION = "Это ваш номер телефона?\n<b>{phone}</b>"


class IMessage(Messages):
    @classmethod
    def start(cls, username: str) -> str:
        return cls.START_MESSAGE.format(username=username)

    @classmethod
    def phone_question(cls, phone: str) -> str:
        return cls.PHONE_QUESTION.format(phone=phone)
