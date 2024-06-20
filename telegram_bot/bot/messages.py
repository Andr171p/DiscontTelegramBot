class MessageInterface:
    def __init__(self, username=None, order_status_response=None):
        # telegram username:
        self.username = username
        # order status response:
        self.order_status_response = order_status_response
        # register messages:
        self.already_register_message = "Вы уже зарегистрированы..."
        self.start_register_message = "Для регистрации просто введите свой номер телефона"
        self.success_register_message = "Вы успешно зарегистрированы"
        self.check_phone_number_message = "Это ваш номер телефона?\n"
        self.input_phone_number_message = ("Введите свой номер телефона начиная с цифры '7'\n"
                                           "Пример: 79998885533")
        # order status:
        self.search_order_message = "Идёт поиск заказа..."
        self.empty_order_message = "У вас пока нет заказа..."

    def start_message(self):
        return f"Здравствуйте, {self.username}! Вам нужно пройти регистрацию. Это займёт всего пару секунд"

    def order_status_message(self):
        return f"Статус вашего заказа: <b>{self.order_status_response[0][0]}</b>"

