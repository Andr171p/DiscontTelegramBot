import requests

from backend.requests1C.webhook_parameters import WebHookRequestsParameters
from backend.requests1C.webhook_parameters import WebHookAPICommands

from misc.utils import format_phone_number


'''# return only one client orders from phone number:
def get_order_response(client_phone_number):
    formated_phone_number = format_phone_number(client_phone_number)

    url = 'https://noname-sushi.online/web/hs/hook?token=NTAxNGVhNWMtZTUwYi00NTdjLTk5NTctNmIyMmM2N2U5NzRh'

    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    data = {
        'command': 'status',
        'telefon': f'{formated_phone_number}'
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()


# return all today orders at the moment:
def get_all_orders_response():
    url = 'https://noname-sushi.online/web/hs/hook?token=NTAxNGVhNWMtZTUwYi00NTdjLTk5NTctNmIyMmM2N2U5NzRh'

    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    data = {
        'command': 'statuses',
        'active': 'true'
    }
    try:
        response = requests.post(url, headers=headers, json=data)

        return response.json()
    except Exception as _ex:
        print(f"ERROR from server: {response.content}\n"
              f"{_ex}")
        return -1


print(get_all_orders_response())'''


class WebHookRequests1C:
    def __init__(self):
        self.url = WebHookRequestsParameters.url
        self.headers = WebHookRequestsParameters.headers
        self.webhook_api_commands = WebHookAPICommands

    # this method return json from post requests:
    def json_response(self, data, timeout=None):
        if timeout is None:
            response = requests.post(
                url=self.url,
                headers=self.headers,
                json=data
            )
        else:
            response = requests.post(
                url=self.url,
                headers=self.headers,
                json=data,
                timeout=timeout
            )
        if self.is_ok(response=response):
            return response.json()
        else:
            return -1

    @staticmethod
    def is_ok(response):
        response_status_code = response.status_code
        print(f"[status code] : {response_status_code}")
        if response_status_code == 200:
            return True
        else:
            print(f"[response.status_code] : {response_status_code}")
            return -1

    # return only one client orders from phone number:
    def get_order_response(self, phone_number):
        telefon = format_phone_number(
            phone_number=phone_number
        )
        data = {
            'command': f'{self.webhook_api_commands.order_status_command}',
            'telefon': f'{telefon}'
        }
        response = self.json_response(
            data=data
        )
        return response

    # return all today orders at the moment:
    def get_all_orders_response(self, timeout=10):
        data = {
            'command': f'{self.webhook_api_commands.all_orders_status_command}',
            'active': 'true'
        }
        try:
            response = self.json_response(
                data=data,
                timeout=timeout
            )
            return response
        except requests.exceptions.Timeout as _ex:
            raise _ex
