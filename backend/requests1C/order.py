import requests

from misc.utils import format_phone_number


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


print(get_order_response("89829764729"))