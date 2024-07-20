import json

from backend.requests1C.webhook_response import get_order_response


class ClientFlyer:
    def __init__(self, client_phone_number):
        self.client_phone_number = client_phone_number
        self.response = get_order_response(
            client_phone_number=self.client_phone_number
        )

    def response_json_to_dict(self):
        flyer_json = json.dumps(self.response, ensure_ascii=False)
        flyer_dict = json.loads(flyer_json)
        return flyer_dict

    def extract_data(self):
        flyer_dict = self.response_json_to_dict()
        flyer_status_data = FlyerStatusData()
        data = flyer_status_data.data
        try:
            orders = flyer_dict['data']['orders']
            for order in orders:
                if order['project'] != 'Дисконт Суши':
                    data['bonus_chips'].append(order['bonus_chips'])
                    data['bonus_flyers'].append(order['bonus_flyers'])

            return data
        except Exception as _ex:
            print(_ex)
            return -1

    def get_flyer_status(self):
        data = self.extract_data()
        bonus_chips = data['bonus_chips'][-1]
        bonus_flyers = data['bonus_flyers'][-1]
        return [bonus_chips, bonus_flyers]


class FlyerStatusData:
    def __init__(self):
        self.data = {
            'bonus_chips': [],
            'bonus_flyers': []
        }

    def clear_values(self):
        for value in self.data.values():
            del value[:]

    def is_empty(self):
        states = []
        for value in self.data.values():
            if value:
                states.append(0)
            else:
                states.append(1)
        if len(self.data) == sum(states):
            return True
        else:
            return False
