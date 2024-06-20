import requests


url = 'https://noname-sushi.online/web/hs/hook?token=NTAxNGVhNWMtZTUwYi00NTdjLTk5NTctNmIyMmM2N2U5NzRh'

headers = {
    'Content-Type': 'application/json; charset=UTF-8'
}

data = {
    'command': 'status',
    'telefon': '+7(982)971-43-72'
}

response = requests.post(url, headers=headers, json=data)

print(response.json())
