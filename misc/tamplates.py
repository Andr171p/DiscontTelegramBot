class StatusMessage:
    accepted_operator = "Принят оператором"
    transferred_to_the_kitchen = "Передан на кухню"
    prepare = "Готовится"
    cooked = "Приготовлен"
    staffed = "Укомплектован"
    ready_for_pickup = "Готов для выдачи"
    sent_to_courier = "Передан курьеру"
    delivered = "Доставлен"
    finished = "Завершен"
    canceled = "Отменен"


class MessageTemplate:
    def __init__(self, order: dict) -> None:
        self.status = order['status']
        self.number = order['number']
        self.delivery_time_from = order['delivery_time_from']
        self.delivery_time_to = order['delivery_time_to']
        self.amount = order['amount']
        self.pay_status = order['pay_status']
        self.cooking_time_to = order['cooking_time_to']
        self.trade_point = order['trade_point']
        self.delivery_method = order['delivery_method']
        self.date = order['date']
        self.trade_point_card = order['trade_point_card']
        self.delivery_adress = order['delivery_adress']
        self.pay_link = order['pay_link']

    def format(self, message: str) -> dict:
        return {
            'message': message,
            'pay_link': self.pay_link
        }

    def pretty_pay_status(self) -> str:
        if self.pay_status == 'CONFIRMED':
            return 'оплачен'
        else:
            return 'не оплачен'

    def message(self) -> dict:
        match self.status:
            case StatusMessage.accepted_operator:
                if self.delivery_method == 'Курьер':
                    message = (f"Ваш заказ №{self.number} принят и будет\n"
                               f"доставлен {self.date} с {self.delivery_time_from} до {self.delivery_time_to} по адресу\n"
                               f"{self.delivery_adress}."
                               f"Сумма: {self.amount} руб.")
                    return self.format(message=message)
                else:
                    message = (f"Ваш заказ №{self.number} принят и будет\n"
                               f"готов к выдаче {self.date} с {self.delivery_time_from} до {self.delivery_time_to} по адресу {self.trade_point}.")
                    return self.format(message=message)
            case StatusMessage.transferred_to_the_kitchen:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()} и\n"
                           f"передан на кухню")
                return self.format(message=message)
            case StatusMessage.prepare:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()} и\n"
                           f"уже готовиться. Время готовности {self.cooking_time_to}")
                return self.format(message=message)
            case StatusMessage.cooked:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()}\n"
                           f"и уже приготовлен. Мы начинаем его готовить к отправке.")
                return self.format(message=message)
            case StatusMessage.staffed:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()} и\n"
                           f"готов к отправке.")
                return self.format(message=message)
            case StatusMessage.sent_to_courier:
                message = (f"Ваш заказ №{self.number} {self.pretty_pay_status()}\n"
                           f"и передан курьеру. Ожидайте доставку с {self.delivery_time_from} до {self.delivery_time_to}\n"
                           f"по адресу:\n"
                           f"{self.delivery_adress}")
                return self.format(message=message)
            case StatusMessage.delivered:
                message = (f"Ваш заказ №{self.number} доставлен курьером.\n"
                           f"Спасибо, сто воспользовались услугами нашего сервиса.")
                return self.format(message=message)
            case StatusMessage.ready_for_pickup:
                message = (f"Ваш заказ {self.number} {self.pretty_pay_status()}\n"
                           f"ожидает вас по адресу: {self.trade_point}\n"
                           f"{self.trade_point_card}")
                return self.format(message=message)
            case StatusMessage.finished:
                message = (f"Ваш заказ №{self.number} успешно завершен. Спасибо,  что\n"
                           f"воспользовались услугами нашего сервиса.\n"
                           f"\n"
                           f"Мы очень старались оставить о нас приятное впечатление\n"
                           f"и будем признательны, если Вы оставите честный отзыв о\n"
                           f"нашей работе в 2ГИС {self.trade_point_card}. Никаких бонусов и\n"
                           f"подарков мы не предлагаем, нам важна справедливая оценка. ")
                return self.format(message=message)
            case StatusMessage.canceled:
                message = (f"Ваш заказ №{self.number} отменен. Нам очень жаль. Надеемся,\n"
                           f"на скорую встречу.")
                return self.format(message=message)


def flyers_template(flyer) -> str:
    template = (f"флаеры: {flyer['flyers']}\n"
                f"фишки: {flyer['chips']}")
    return template