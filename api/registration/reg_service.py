from api.http_session import HTTPSession
from api.registration.reg_request import (
    RegistrationRequest,
    RegistrationEndPoints
)

from misc.utils import json_to_dict

from typing import List


class RegistrationAPI(HTTPSession):
    reg_request = RegistrationRequest()
    end_points = RegistrationEndPoints()

    def url(self, end_point: str) -> str:
        url = f"{self.reg_request.REGISTRATION_URL}{self.reg_request.PREFIX}{end_point}"
        return url

    async def get_user(self, user_id: int) -> dict:
        url = self.url(end_point=self.end_points.GET_USER)
        data = {
            'user_id': user_id
        }
        response = await self.post_request(
            url=url,
            data=data
        )
        user = json_to_dict(_json=response)
        return user

    async def get_users(self) -> List[dict]:
        url = self.url(end_point=self.end_points.GET_USERS)
        response = await self.get_request(url=url)
        users = json_to_dict(_json=response)
        return users

    async def create_user(
            self, user_id: int, username: str, phone: str
    ) -> dict:
        url = self.url(end_point=self.end_points.CREATE_USER)
        data = {
            'user_id': user_id,
            'username': username,
            'telefon': phone
        }
        response = await self.post_request(
            url=url,
            data=data
        )
        user = json_to_dict(_json=response)
        return user

    async def check_user(self, user_id: int) -> bool:
        url = self.url(end_point=self.end_points.CHECK_USER)
        data = {
            'user_id': user_id
        }
        response = await self.post_request(
            url=url,
            data=data
        )
        exists = json_to_dict(_json=response)
        return exists

    async def get_phone(self, user_id: int) -> str:
        url = self.url(end_point=self.end_points.GET_PHONE)
        data = {
            'user_id': user_id
        }
        response = await self.post_request(
            url=url,
            data=data
        )
        phone = json_to_dict(_json=response)
        return phone

    async def replace_phone(self, user_id: int, phone: str) -> bool:
        url = self.url(end_point=self.end_points.REPLACE_USER)
        data = {
            'user_id': user_id,
            'phone': phone
        }
        response = await self.post_request(
            url=url,
            data=data
        )
        user = json_to_dict(_json=response)
        return bool(user)


registration_api = RegistrationAPI()
