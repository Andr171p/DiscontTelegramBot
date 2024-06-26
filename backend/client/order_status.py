import json

from backend.requests1C.order import get_order_response

from misc.utils import format_order_number, format_order_time
from misc.utils import format_order_date, format_trade_card


class ClientOrder:
    def __init__(self, client_phone_number):
        self.client_phone_number = client_phone_number
        self.response = get_order_response(
            client_phone_number=self.client_phone_number
        )
        self.order_dict = None
        self.status_data = None

    def response_json_to_dict(self):
        order_json = json.dumps(self.response, ensure_ascii=False)
        self.order_dict = json.loads(order_json)

    def order_info_data(self):
        try:
            # orders = self.order_dict['data']['orders'][0]

            status_data_class = StatusData()
            self.status_data = status_data_class.status_data
            if status_data_class.is_empty() != 1:
                status_data_class.clear_values()

            orders = self.order_dict['data']['orders']
            for order in orders:
                if order['project'] == 'Дисконт Суши':
                    self.status_data['number'].append(order['number'])
                    self.status_data['status'].append(order['status'])
                    self.status_data['amount'].append(order['amount'])
                    self.status_data['pay_status'].append(order['pay_status'])
                    self.status_data['pay_link'].append(order['pay_link'])
                    self.status_data['cooking_time_to'].append(order['cooking_time_to'])
                    self.status_data['delivery_time_from'].append(order['delivery_time_from'])
                    self.status_data['delivery_time_to'].append(order['delivery_time_to'])
                    self.status_data['trade_point'].append(order['trade_point'])
                    self.status_data['delivery_method'].append(order['delivery_method'])
                    self.status_data['date'].append(order['date'])
                    self.status_data['trade_point_card'].append(order['trade_point_card'])
                    self.status_data['delivery_adress'].append(order['delivery_adress'])
                    self.status_data['project'].append(order['project'])

        except Exception as _ex:
            print(_ex)
            self.status_data = -1

    def get_order_status(self):
        self.response_json_to_dict()
        self.order_info_data()

        if self.status_data == -1:
            return -1
        else:
            status_response = []
            item_status_length = len(list(self.status_data.values())[0])
            for i in range(item_status_length):
                pretty_status = PrettyStatus(
                    status=self.status_data['status'][i],
                    number_of_order=self.status_data['number'][i],
                    first_delivery_time=self.status_data['delivery_time_from'][i],
                    second_delivery_time=self.status_data['delivery_time_to'][i],
                    order_summ=self.status_data['amount'][i],
                    pay_status=self.status_data['pay_status'][i],
                    cooking_time_to=self.status_data['cooking_time_to'][i],
                    trade_point=self.status_data['trade_point'][i],
                    delivery_method=self.status_data['delivery_method'][i],
                    date=self.status_data['date'][i],
                    trade_point_card=self.status_data['trade_point_card'][i],
                    delivery_adress=self.status_data['delivery_adress'][i]
                )
                status = pretty_status.message()

                if self.status_data['pay_status'][i] == 'CONFIRMED':
                    status_response.append([status])
                elif self.status_data['status'][i] == 'Завершен':
                    status_response.append([status])
                else:
                    status_response.append(
                        [status, self.status_data['pay_link'][i]]
                    )

            return status_response


class PrettyStatus:
    def __init__(self,
                 status,
                 number_of_order,
                 first_delivery_time,
                 second_delivery_time,
                 order_summ,
                 pay_status,
                 cooking_time_to,
                 trade_point,
                 delivery_method,
                 date,
                 trade_point_card,
                 delivery_adress
                 ):
        self.status = status
        self.number_of_order = format_order_number(number_of_order)
        self.first_delivery_time = format_order_time(first_delivery_time)
        self.second_delivery_time = format_order_time(second_delivery_time)
        self.order_summ = order_summ
        self.pay_status = pay_status
        self.cooking_time_to = format_order_time(cooking_time_to)
        self.trade_point = trade_point
        self.delivery_method = delivery_method
        self.date = format_order_date(date)
        self.trade_point_card = format_trade_card(trade_point_card)
        self.delivery_adress = delivery_adress

    def pretty_pay_status(self):
        if self.pay_status == 'CONFIRMED':
            return 'оплачен'
        else:
            return 'не оплачен'

    def message(self):
        match self.status:
            case StatusMessage.accepted_operator:
                if self.delivery_method == 'Курьер':
                    message = (f"Ваш заказ №{self.number_of_order} принят и будет\n"
                                f"доставлен {self.date} с {self.first_delivery_time} до {self.second_delivery_time} по адресу\n"
                               f"{self.delivery_adress}."
                                f"Сумма: {self.order_summ} руб.")
                    return message
                else:
                    message = (f"Ваш заказ №{self.number_of_order} принят и будет\n"
                               f"готов к выдаче {self.date} с {self.first_delivery_time} до {self.second_delivery_time} по адресу {self.trade_point}.")
                    return message
            case StatusMessage.transferred_to_the_kitchen:
                message = (f"Ваш заказ №{self.number_of_order} {self.pretty_pay_status()} и\n"
                           f"передан на кухню")
                return message
            case StatusMessage.prepare:
                message = (f"Ваш заказ №{self.number_of_order} {self.pretty_pay_status()} и\n"
                           f"уже готовиться. Время готовности {self.cooking_time_to}")
                return message
            case StatusMessage.cooked:
                message = (f"Ваш заказ №{self.number_of_order} {self.pretty_pay_status()}\n"
                           f"и уже приготовлен. Мы начинаем его готовить к отправке.")
                return message
            case StatusMessage.staffed:
                message = (f"Ваш заказ №{self.number_of_order} {self.pretty_pay_status()} и\n"
                           f"готов к отправке.")
                return message
            case StatusMessage.sent_to_courier:
                message = (f"Ваш заказ №{self.number_of_order} {self.pretty_pay_status()}\n"
                           f"и передан курьеру. Ожидайте доставку с {self.first_delivery_time} до {self.second_delivery_time}\n"
                           f"по адресу:\n"
                           f"{self.delivery_adress}")
                return message
            case StatusMessage.delivered:
                message = (f"Ваш заказ №{self.number_of_order} доставлен курьером.\n"
                           f"Спасибо, сто воспользовались услугами нашего сервиса.")
                return message
            case StatusMessage.ready_for_pickup:
                message = (f"Ваш заказ {self.number_of_order} {self.pretty_pay_status()}\n"
                           f"ожидает вас по адресу: {self.trade_point}\n"
                           f"{self.trade_point_card}")
                return message
            case StatusMessage.finished:
                message = (f"Ваш заказ №{self.number_of_order} успешно завершен. Спасибо,  что\n"
                           f"воспользовались услугами нашего сервиса.\n"
                           f"\n"
                           f"Мы очень старались оставить о нас приятное впечатление\n"
                           f"и будем признательны, если Вы оставите честный отзыв о\n"
                           f"нашей работе в 2ГИС {self.trade_point_card}. Никаких бонусов и\n"
                           f"подарков мы не предлагаем, нам важна справедливая оценка. ")
                return message
            case StatusMessage.canceled:
                message = (f"Ваш заказ №{self.number_of_order} отменен. Нам очень жаль. Надеемся,\n"
                           f"на скорую встречу.")
                return message


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


class StatusData:
    def __init__(self):
        self.status_data = {
            'number': [],
            'status': [],
            'amount': [],
            'pay_status': [],
            'pay_link': [],
            'cooking_time_to': [],
            'delivery_time_from': [],
            'delivery_time_to': [],
            'trade_point': [],
            'delivery_method': [],
            'date': [],
            'trade_point_card': [],
            'delivery_adress': [],
            'project': []
        }

    def clear_values(self):
        for value in self.status_data.values():
            del value[:]

    def is_empty(self):
        states = []
        for value in self.status_data.values():
            if value:
                states.append(0)
            else:
                states.append(1)
        if len(self.status_data) == sum(states):
            return True
        else:
            return False


'''print(ClientOrder(client_phone_number="89829764729").get_order_status())
print(ClientOrder(client_phone_number="89829764729").get_order_status())'''
