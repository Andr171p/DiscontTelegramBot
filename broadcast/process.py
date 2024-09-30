import json
import asyncio

from broadcast.triggers import (
    TriggerProject,
    TriggerStatuses
)

from api.registration.reg_service import registration_api


async def user_id_from_phone(phone: str) -> int:
    user_id = await registration_api.get_user_id(phone=phone)
    return user_id


def check_status(message: dict) -> dict | None:
    project = message['project']
    status = message['status']
    if project == TriggerProject.PROJECT and status in TriggerStatuses.STATUSES:
        return message


class LoadMessage:
    def __init__(self, body: str) -> None:
        self.body = body

    def load(self) -> dict:
        _dict = json.loads(self.body)
        return _dict


class MessageResponse:
    def __init__(self, data: dict) -> None:
        self.data = data

    async def message(self) -> dict:
        return {
            'user_id': await user_id_from_phone(phone=self.data['phone']),
            'message': self.data['message'],
            'pay_link': self.data['pay_link'],
            'status': self.data['status'],
            'project': self.data['project']
        }


class Message(LoadMessage):
    async def message(self) -> dict:
        data = self.load()
        message = await MessageResponse(data=data).message()
        return message